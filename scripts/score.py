"""
Cron script: score any unscored ContentItems via LLM.
Run: python -m scripts.score
Railway: schedule after ingest (e.g. every 2 hours, offset by 30 min).
"""
import asyncio
import logging

from db.models import ContentItem
from db.session import SessionLocal
from ingestion.base import RawItem
from scoring.llm import score_item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BATCH_SIZE = 50


async def run_scoring() -> None:
    db = SessionLocal()
    try:
        unscored = (
            db.query(ContentItem)
            .filter(ContentItem.quality_score.is_(None))
            .order_by(ContentItem.published_at.desc().nullslast(), ContentItem.ingested_at.desc())
            .limit(BATCH_SIZE)
            .all()
        )
        logger.info("Scoring %d unscored items", len(unscored))

        for item in unscored:
            try:
                raw = RawItem(
                    source=item.source,
                    source_id=item.source_id,
                    url=item.url,
                    title=item.title,
                    body_text=item.body_text,
                )
                scores = await score_item(raw)
                item.quality_score = scores["quality_score"]
                item.authenticity_score = scores["authenticity_score"]
                item.anxiety_score = scores["anxiety_score"]
                item.metadata_json = {
                    **(item.metadata_json or {}),
                    "why_this": scores.get("why_this", ""),
                }
            except Exception as e:
                logger.error("Failed to score item %s: %s", item.source_id, e)

        db.commit()
        logger.info("Scoring complete")
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(run_scoring())
