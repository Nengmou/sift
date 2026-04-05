"""
Cron script: send daily digest emails to users whose delivery_time has arrived.
Run: python -m scripts.deliver
Railway: schedule every 15 minutes to catch all delivery time windows.
"""
import logging
from datetime import datetime, timezone

from db.models import ContentItem, User
from db.session import SessionLocal
from delivery.email import send_digest
from scoring.ranker import rank_items_for_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOP_N_ITEMS = 15  # Items to pull from DB before ranking
EMAIL_PICKS = 10  # Items to include in the email


def run_delivery() -> None:
    db = SessionLocal()
    now_utc = datetime.now(timezone.utc)
    current_hhmm = now_utc.strftime("%H:%M")

    try:
        users = (
            db.query(User)
            .filter(User.delivery_time == current_hhmm)
            .all()
        )
        logger.info("Delivering to %d users at %s UTC", len(users), current_hhmm)

        for user in users:
            try:
                items = (
                    db.query(ContentItem)
                    .filter(ContentItem.quality_score.isnot(None))
                    .order_by(
                        ContentItem.quality_score.desc(),
                        ContentItem.ingested_at.desc(),
                    )
                    .limit(TOP_N_ITEMS)
                    .all()
                )
                ranked = rank_items_for_user(items, user)[:EMAIL_PICKS]
                if ranked:
                    message_id = send_digest(user, ranked)
                    logger.info("Delivered to %s — %s", user.email, message_id)
                else:
                    logger.warning("No ranked items for %s, skipping", user.email)
            except Exception as e:
                logger.error("Failed to deliver to %s: %s", user.email, e)
    finally:
        db.close()


if __name__ == "__main__":
    run_delivery()
