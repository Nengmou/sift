"""Combines LLM scores into a composite rank for a given user."""
import math
from datetime import UTC, datetime, timedelta
from urllib.parse import urlsplit

from config.sources import TAG_TO_INTEREST
from db.models import ContentItem, User
from ingestion.base import Source


def _normalized_domain(url: str) -> str:
    parts = urlsplit(url)
    host = (parts.netloc or "unknown").lower()
    if host.startswith("www."):
        host = host[4:]
    return host or "unknown"


def _publisher_key(item: ContentItem) -> str:
    if item.source == Source.REDDIT:
        subreddit = str(item.metadata_json.get("subreddit", "")).strip()
        return f"reddit:{subreddit or 'unknown'}"
    if item.source == Source.YOUTUBE:
        channel_id = str(item.metadata_json.get("channel_id", "")).strip()
        return f"youtube:{channel_id or 'unknown'}"
    if item.source == Source.TWITTER:
        author = (item.author or "").strip().lstrip("@").lower()
        return f"twitter:{author or 'unknown'}"

    url = (
        str(item.metadata_json.get("canonical_url", "")).strip()
        or (item.url or "").strip()
    )
    if not url:
        return f"{item.source}:unknown"
    return f"{item.source}:{_normalized_domain(url)}"


def _available_source_count(items: list[ContentItem]) -> int:
    return len({item.source for item in items})



def _relevance_score(item: ContentItem, user: User) -> float:
    """
    Relevance of the item to the user's interests, as a float in [0, 1].

    Sums the LLM-assigned relevance scores of tags that map to a user interest,
    capped at 1.0. Items with no matching tags score 0.
    When the user has no interests configured, return 1.0 (show everything).
    """
    interests = {i.lower().strip() for i in user.interests if i.strip()}
    if not interests:
        return 1.0

    tags = (item.metadata_json or {}).get("tags", [])[:3]
    if not tags:
        return 0.05
    matched_relevance = sum(
        t["relevance"]
        for t in tags
        if isinstance(t, dict) and TAG_TO_INTEREST.get(t.get("tag", ""), "").lower() in interests
    )
    return matched_relevance / len(tags)


_FRESHNESS_HALF_LIFE_DAYS = 7.0


def _freshness_score(item: ContentItem) -> float:
    """Exponential decay: 1.0 today, ~0.5 at 7 days, ~0.25 at 14 days."""
    ts = item.published_at or getattr(item, "ingested_at", None)
    if ts is None:
        return 0.5
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=UTC)
    age_days = max(0.0, (datetime.now(UTC) - ts).total_seconds() / 86400)
    return math.pow(0.5, age_days / _FRESHNESS_HALF_LIFE_DAYS)


def compute_rank(item: ContentItem, user: User) -> float:
    """
    Composite rank score for `item` relative to `user`.

    score = relevance × freshness × (0.5×auth + 0.3×calm + 0.2×quality)

    Relevance personalizes by interest. Freshness applies exponential
    decay (7-day half-life). Quality weights reflect editorial bias
    toward authentic, calm practitioner voices.
    """
    q = item.quality_score or 0.0
    a = item.authenticity_score or 0.0
    c = item.calmness_score or 0.0
    r = _relevance_score(item, user)
    f = _freshness_score(item)
    return round(r * f * (0.5 * a + 0.3 * c + 0.2 * q), 4)


def _apply_caps(
    scored_items: list[ContentItem],
    max_per_platform: int,
    max_per_publisher: int,
    shortlist_max_per_publisher: int,
    max_per_content_type: int,
) -> list[ContentItem]:
    shortlist: list[ContentItem] = []
    shortlist_publisher_counts: dict[str, int] = {}
    for item in scored_items:
        publisher = _publisher_key(item)
        publisher_count = shortlist_publisher_counts.get(publisher, 0)
        if publisher_count < shortlist_max_per_publisher:
            shortlist.append(item)
            shortlist_publisher_counts[publisher] = publisher_count + 1

    platform_counts: dict[str, int] = {}
    publisher_counts: dict[str, int] = {}
    content_type_counts: dict[str, int] = {}
    ranked: list[ContentItem] = []
    for item in shortlist:
        platform_count = platform_counts.get(item.source, 0)
        publisher = _publisher_key(item)
        publisher_count = publisher_counts.get(publisher, 0)
        content_type = item.content_type or "unknown"
        type_count = content_type_counts.get(content_type, 0)
        if (
            platform_count < max_per_platform
            and publisher_count < max_per_publisher
            and type_count < max_per_content_type
        ):
            ranked.append(item)
            platform_counts[item.source] = platform_count + 1
            publisher_counts[publisher] = publisher_count + 1
            content_type_counts[content_type] = type_count + 1

    return ranked


def fetch_candidates(db, lookback_days: int = 30, per_platform: int = 200) -> list[ContentItem]:
    """
    Fetch candidate items for ranking: most recent scored items per
    platform within `lookback_days`. Used by both web feed and email digest.
    """
    since = datetime.now(UTC) - timedelta(days=lookback_days)
    items_by_id: dict[str, ContentItem] = {}
    for source in Source:
        batch = (
            db.query(ContentItem)
            .filter(
                ContentItem.quality_score.isnot(None),
                ContentItem.published_at >= since,
                ContentItem.source == source,
            )
            .order_by(ContentItem.published_at.desc().nullslast())
            .limit(per_platform)
            .all()
        )
        for item in batch:
            items_by_id[item.id] = item
    return list(items_by_id.values())


def rank_items_for_user(
    items: list[ContentItem],
    user: User,
    max_per_platform: int = 3,
    max_per_publisher: int = 2,
    shortlist_max_per_publisher: int = 5,
    max_per_content_type: int = 8,
    target_min_items: int = 8,
) -> list[ContentItem]:
    """
    Return items sorted by composite rank with diversity enforced.

    `max_per_platform` caps whole sources (`rss`, `reddit`, etc.) in the final list.
    `max_per_publisher` caps repeated publishers/communities/channels/accounts
    in the final list.
    `shortlist_max_per_publisher` caps publisher contribution before final selection.
    """
    available_sources = _available_source_count(items)
    effective_max_per_platform = max_per_platform
    if available_sources <= 1:
        effective_max_per_platform = 20
    elif available_sources == 2:
        effective_max_per_platform = max(max_per_platform, 10)

    scored_items = sorted(items, key=lambda i: compute_rank(i, user), reverse=True)
    strategies = [
        (effective_max_per_platform, max_per_publisher, shortlist_max_per_publisher),
        (effective_max_per_platform + 1, max_per_publisher, shortlist_max_per_publisher),
        (effective_max_per_platform + 2, max_per_publisher, shortlist_max_per_publisher),
        (effective_max_per_platform + 2, max_per_publisher + 1, shortlist_max_per_publisher),
        (effective_max_per_platform + 2, max_per_publisher + 1, shortlist_max_per_publisher + 2),
    ]

    best_ranked: list[ContentItem] = []
    for platform_cap, publisher_cap, shortlist_publisher_cap in strategies:
        ranked = _apply_caps(
            scored_items=scored_items,
            max_per_platform=platform_cap,
            max_per_publisher=publisher_cap,
            shortlist_max_per_publisher=shortlist_publisher_cap,
            max_per_content_type=max_per_content_type,
        )
        if len(ranked) > len(best_ranked):
            best_ranked = ranked
        if len(ranked) >= target_min_items:
            return ranked

    return best_ranked
