"""
Cron script: send daily digest emails to users whose delivery_time has arrived.
Run: python -m scripts.deliver
Railway: schedule every 15 minutes to catch all delivery time windows.
"""
import logging
from datetime import UTC, datetime

from db.models import User
from db.session import SessionLocal
from delivery.email import send_digest
from scoring.ranker import fetch_candidates, rank_items_for_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

EMAIL_PICKS = 5    # items included in the final email


def run_delivery() -> None:
    db = SessionLocal()
    now_utc = datetime.now(UTC)
    current_hhmm = now_utc.strftime("%H:%M")

    try:
        users = db.query(User).filter(User.delivery_time == current_hhmm).all()
        logger.info("Delivering to %d users at %s UTC", len(users), current_hhmm)

        for user in users:
            try:
                candidates = fetch_candidates(db)
                ranked = rank_items_for_user(candidates, user, target_size=EMAIL_PICKS)
                if ranked:
                    message_id = send_digest(user, ranked)
                    logger.info(
                        "Delivered to %s (%d items) — %s",
                        user.email, len(ranked), message_id,
                    )
                else:
                    logger.warning("No ranked items for %s — skipping", user.email)
            except Exception as e:
                logger.error("Failed to deliver to %s: %s", user.email, e)
    finally:
        db.close()


if __name__ == "__main__":
    run_delivery()
