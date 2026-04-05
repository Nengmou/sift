"""
Cron script: send daily digest emails to users whose delivery_time has arrived.
Run: python -m scripts.deliver
Railway: schedule every 15 minutes to catch all delivery time windows.
"""
import logging
from datetime import datetime, timedelta, timezone

from db.models import ContentItem, User
from db.session import SessionLocal
from delivery.email import send_digest
from scoring.ranker import rank_items_for_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CANDIDATE_POOL = 100  # items pulled from DB per user before ranking
EMAIL_PICKS = 10      # items included in the final email
LOOKBACK_DAYS = 2     # only consider items ingested in the last N days


def _fetch_candidates(db, user: User) -> list[ContentItem]:
    """
    Pull scored items from the last LOOKBACK_DAYS days.
    If the user has interests, prefer items whose text overlaps — but always
    fall back to the full pool so the feed is never empty.
    """
    since = datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)

    base_query = (
        db.query(ContentItem)
        .filter(
            ContentItem.quality_score.isnot(None),
            ContentItem.ingested_at >= since,
        )
        .order_by(ContentItem.quality_score.desc())
    )

    if user.interests:
        # Build a simple LIKE filter across title + body for each interest keyword
        from sqlalchemy import or_
        filters = []
        for interest in user.interests:
            keyword = f"%{interest.lower()}%"
            filters.append(ContentItem.title.ilike(keyword))
            filters.append(ContentItem.body_text.ilike(keyword))
        interest_matches = base_query.filter(or_(*filters)).limit(CANDIDATE_POOL).all()

        if len(interest_matches) >= EMAIL_PICKS:
            return interest_matches

        # Not enough interest-matched items — pad with top-quality items
        matched_ids = {item.id for item in interest_matches}
        remainder = (
            base_query
            .filter(ContentItem.id.notin_(matched_ids))
            .limit(CANDIDATE_POOL - len(interest_matches))
            .all()
        )
        return interest_matches + remainder

    return base_query.limit(CANDIDATE_POOL).all()


def run_delivery() -> None:
    db = SessionLocal()
    now_utc = datetime.now(timezone.utc)
    current_hhmm = now_utc.strftime("%H:%M")

    try:
        users = db.query(User).filter(User.delivery_time == current_hhmm).all()
        logger.info("Delivering to %d users at %s UTC", len(users), current_hhmm)

        for user in users:
            try:
                candidates = _fetch_candidates(db, user)
                ranked = rank_items_for_user(candidates, user)[:EMAIL_PICKS]
                if ranked:
                    message_id = send_digest(user, ranked)
                    logger.info("Delivered to %s (%d items) — %s", user.email, len(ranked), message_id)
                else:
                    logger.warning("No ranked items for %s — skipping", user.email)
            except Exception as e:
                logger.error("Failed to deliver to %s: %s", user.email, e)
    finally:
        db.close()


if __name__ == "__main__":
    run_delivery()
