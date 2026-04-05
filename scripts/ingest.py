"""
Cron script: fetch content from all sources and persist to DB.
Run: python -m scripts.ingest
Railway: schedule every 2–4 hours.
"""
import asyncio
import logging
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from config.settings import get_settings
from config.sources import RSS_FEEDS, SUBREDDITS, TWITTER_ACCOUNTS, YOUTUBE_CHANNEL_IDS
from db.models import ContentItem
from db.session import SessionLocal
from ingestion.hn import HNConnector
from ingestion.rss import RSSConnector
from ingestion.reddit import RedditConnector
from ingestion.twitter import TwitterConnector
from ingestion.youtube import YouTubeConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RECENT_DEDUPE_WINDOW = 500
TRACKING_PARAMS = {
    "utm_source",
    "utm_medium",
    "utm_campaign",
    "utm_term",
    "utm_content",
    "ref",
    "ref_src",
    "source",
}


def canonicalize_url(url: str) -> str:
    if not url:
        return ""

    parts = urlsplit(url.strip())
    filtered_query = [
        (key, value)
        for key, value in parse_qsl(parts.query, keep_blank_values=True)
        if key.lower() not in TRACKING_PARAMS
    ]
    normalized_query = urlencode(sorted(filtered_query))
    path = parts.path.rstrip("/") or "/"

    return urlunsplit(
        (
            parts.scheme.lower() or "https",
            parts.netloc.lower(),
            path,
            normalized_query,
            "",
        )
    )


def normalize_title(title: str | None) -> str:
    if not title:
        return ""
    return " ".join(title.lower().split())


def is_duplicate(raw_url: str, raw_title: str | None, existing: ContentItem) -> bool:
    if canonicalize_url(raw_url) and canonicalize_url(raw_url) == canonicalize_url(existing.url):
        return True

    normalized_raw_title = normalize_title(raw_title)
    normalized_existing_title = normalize_title(existing.title)
    if normalized_raw_title and normalized_existing_title:
        similarity = SequenceMatcher(None, normalized_raw_title, normalized_existing_title).ratio()
        if similarity >= 0.97:
            return True

    return False


def load_recent_items(db: SessionLocal) -> list[ContentItem]:
    return (
        db.query(ContentItem)
        .order_by(ContentItem.ingested_at.desc())
        .limit(RECENT_DEDUPE_WINDOW)
        .all()
    )


async def run_ingestion() -> None:
    settings = get_settings()
    connectors = [
        HNConnector(),
        RSSConnector(feed_urls=RSS_FEEDS),
        RedditConnector(subreddits=SUBREDDITS),
    ]
    if settings.has_twitter and TWITTER_ACCOUNTS:
        connectors.append(
            TwitterConnector(
                bearer_token=settings.twitter_bearer_token,
                usernames=TWITTER_ACCOUNTS,
            )
        )
    if settings.has_youtube and YOUTUBE_CHANNEL_IDS:
        connectors.append(
            YouTubeConnector(
                api_key=settings.youtube_api_key,
                channel_ids=YOUTUBE_CHANNEL_IDS,
            )
        )

    db = SessionLocal()
    total_new = 0
    try:
        recent_items = load_recent_items(db)

        for connector in connectors:
            try:
                items = await connector.fetch()
                connector_new = 0
                connector_duplicates = 0
                for raw in items:
                    existing = (
                        db.query(ContentItem)
                        .filter_by(source=raw.source, source_id=raw.source_id)
                        .first()
                    )
                    if not existing:
                        if any(is_duplicate(raw.url, raw.title, candidate) for candidate in recent_items):
                            connector_duplicates += 1
                            continue

                        item = ContentItem(
                            source=raw.source,
                            source_id=raw.source_id,
                            url=raw.url,
                            title=raw.title,
                            author=raw.author,
                            body_text=raw.body_text,
                            published_at=raw.published_at,
                            content_type=raw.content_type,
                            metadata_json={
                                **(raw.metadata or {}),
                                "canonical_url": canonicalize_url(raw.url),
                            },
                        )
                        db.add(item)
                        recent_items.insert(0, item)
                        recent_items = recent_items[:RECENT_DEDUPE_WINDOW]
                        total_new += 1
                        connector_new += 1
                db.commit()
                logger.info(
                    "%s: fetched=%d new=%d duplicates=%d",
                    connector.__class__.__name__,
                    len(items),
                    connector_new,
                    connector_duplicates,
                )
            except NotImplementedError:
                logger.info("%s: skipped (not yet implemented)", connector.__class__.__name__)
            except Exception as e:
                logger.error("%s: failed — %s", connector.__class__.__name__, e)
                db.rollback()
                recent_items = load_recent_items(db)
    finally:
        db.close()

    logger.info("Ingestion complete — %d new items", total_new)


if __name__ == "__main__":
    asyncio.run(run_ingestion())
