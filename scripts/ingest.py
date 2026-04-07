"""
Cron script: fetch content from all sources and persist to DB.
Run: python -m scripts.ingest
Railway: schedule every 2–4 hours.
"""
import argparse
import asyncio
import logging
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from config.settings import get_settings
from config.sources import RSS_FEEDS, SUBREDDITS, TWITTER_ACCOUNTS, YOUTUBE_CHANNEL_IDS
from db.models import ContentItem
from db.session import SessionLocal
from ingestion.base import Source
from ingestion.hn import HNConnector
from ingestion.reddit import RedditConnector
from ingestion.rss import RSSConnector
from ingestion.twitter import TwitterConnector
from ingestion.youtube import YouTubeConnector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SUPPORTED_SOURCES = tuple(Source)

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


def existing_source_ids(
    db: SessionLocal,
    source: str,
    incoming_source_ids: set[str],
) -> set[str]:
    if not incoming_source_ids:
        return set()
    rows = (
        db.query(ContentItem.source_id)
        .filter(
            ContentItem.source == source,
            ContentItem.source_id.in_(incoming_source_ids),
        )
        .all()
    )
    return {row[0] for row in rows}


def build_connectors(selected_sources: set[str] | None = None):
    settings = get_settings()
    selected = selected_sources or set(SUPPORTED_SOURCES)
    connectors = []
    skipped: dict[str, str] = {}

    if "hn" in selected:
        connectors.append(HNConnector())
    if "rss" in selected:
        connectors.append(RSSConnector(feed_urls=RSS_FEEDS))
    if "reddit" in selected:
        connectors.append(RedditConnector(subreddits=SUBREDDITS))
    if "twitter" in selected:
        if settings.has_twitter and TWITTER_ACCOUNTS:
            connectors.append(
                TwitterConnector(
                    bearer_token=settings.twitter_bearer_token,
                    usernames=TWITTER_ACCOUNTS,
                )
            )
        else:
            skipped["twitter"] = (
                "TWITTER_BEARER_TOKEN is not configured"
                if not settings.has_twitter
                else "TWITTER_ACCOUNTS is empty"
            )
    if "youtube" in selected:
        if settings.has_youtube and YOUTUBE_CHANNEL_IDS:
            connectors.append(
                YouTubeConnector(
                    api_key=settings.youtube_api_key,
                    channel_ids=YOUTUBE_CHANNEL_IDS,
                )
            )
        else:
            skipped["youtube"] = (
                "YOUTUBE_API_KEY is not configured"
                if not settings.has_youtube
                else "YOUTUBE_CHANNEL_IDS is empty"
            )

    return connectors, skipped


async def run_ingestion(selected_sources: set[str] | None = None) -> None:
    connectors, skipped = build_connectors(selected_sources)
    explicitly_selected = selected_sources is not None

    if skipped:
        for source, reason in skipped.items():
            if explicitly_selected:
                logger.warning("%s requested but skipped: %s", source, reason)
            else:
                logger.info("%s not enabled: %s", source, reason)

    if explicitly_selected and not connectors:
        raise SystemExit("No requested sources could be enabled with the current configuration.")

    db = SessionLocal()
    total_new = 0
    try:
        recent_items = load_recent_items(db)

        for connector in connectors:
            try:
                items = await connector.fetch()
                pending_new = 0
                connector_duplicates = 0
                incoming_source_ids = {raw.source_id for raw in items}
                seen_source_ids = (
                    existing_source_ids(db, items[0].source, incoming_source_ids)
                    if items
                    else set()
                )
                for raw in items:
                    if raw.source_id in seen_source_ids:
                        connector_duplicates += 1
                        continue

                    if any(
                        is_duplicate(raw.url, raw.title, c) for c in recent_items
                    ):
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
                    seen_source_ids.add(raw.source_id)
                    recent_items.insert(0, item)
                    recent_items = recent_items[:RECENT_DEDUPE_WINDOW]
                    pending_new += 1
                db.commit()
                total_new += pending_new
                logger.info(
                    "%s: fetched=%d new=%d duplicates=%d",
                    connector.__class__.__name__,
                    len(items),
                    pending_new,
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch source content into the Sift database.")
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=SUPPORTED_SOURCES,
        help="Only ingest the specified sources. Defaults to all enabled sources.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_ingestion(set(args.sources) if args.sources else None))
