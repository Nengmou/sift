"""
Cron script: fetch content from all sources and persist to DB.
Run: python -m scripts.ingest
Railway: schedule every 2–4 hours.
"""
import asyncio
import logging

from config.sources import RSS_FEEDS, SUBREDDITS
from db.models import ContentItem
from db.session import SessionLocal
from ingestion.hn import HNConnector
from ingestion.rss import RSSConnector
from ingestion.reddit import RedditConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_ingestion() -> None:
    connectors = [
        HNConnector(),
        RSSConnector(feed_urls=RSS_FEEDS),
        RedditConnector(subreddits=SUBREDDITS),
        # TwitterConnector and YouTubeConnector added when API keys are ready
    ]

    db = SessionLocal()
    total_new = 0
    try:
        for connector in connectors:
            try:
                items = await connector.fetch()
                for raw in items:
                    existing = (
                        db.query(ContentItem)
                        .filter_by(source=raw.source, source_id=raw.source_id)
                        .first()
                    )
                    if not existing:
                        db.add(ContentItem(
                            source=raw.source,
                            source_id=raw.source_id,
                            url=raw.url,
                            title=raw.title,
                            author=raw.author,
                            body_text=raw.body_text,
                            published_at=raw.published_at,
                            content_type=raw.content_type,
                            metadata_json=raw.metadata or {},
                        ))
                        total_new += 1
                db.commit()
                logger.info("%s: ingested %d items", connector.__class__.__name__, len(items))
            except NotImplementedError:
                logger.info("%s: skipped (not yet implemented)", connector.__class__.__name__)
            except Exception as e:
                logger.error("%s: failed — %s", connector.__class__.__name__, e)
                db.rollback()
    finally:
        db.close()

    logger.info("Ingestion complete — %d new items", total_new)


if __name__ == "__main__":
    asyncio.run(run_ingestion())
