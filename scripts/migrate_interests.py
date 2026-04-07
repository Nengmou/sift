"""
One-time migration: remap user interests from old 10-category names to new 35-category names.
Safe to re-run — idempotent (already-migrated interests are unchanged).
Run: python -m scripts.migrate_interests
"""
import logging

from db.models import User
from db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

INTEREST_MAP = {
    "LLM infrastructure": "AI infrastructure & compute",
    "AI agents": "AI agents & automation",
    "MLOps": "MLOps & deployment",
    "Prompt engineering": "Prompt engineering & AI UX",
    "Open-source models": "Open-source AI",
    "Evaluation and testing": "Evaluation & benchmarks",
    "AI for productivity": "AI tools & productivity",
    "Frontend development": "Software engineering",
    "Systems design": "Software engineering",
    "Data engineering": "Data & knowledge",
}


def run_migration() -> None:
    db = SessionLocal()
    try:
        users = db.query(User).all()
        logger.info("Migrating interests for %d users", len(users))
        updated = 0
        for user in users:
            old = list(user.interests or [])
            # Remap each interest, deduplicate while preserving order
            seen: set[str] = set()
            new: list[str] = []
            for interest in old:
                mapped = INTEREST_MAP.get(interest, interest)
                if mapped not in seen:
                    seen.add(mapped)
                    new.append(mapped)
            if new != old:
                logger.info("  %s: %s → %s", user.email, old, new)
                user.interests = new
                updated += 1
        db.commit()
        logger.info("Migration complete — %d users updated", updated)
    finally:
        db.close()


if __name__ == "__main__":
    run_migration()
