"""Combines LLM scores into a composite rank for a given user."""
from urllib.parse import urlsplit

from db.models import ContentItem, User


def _normalized_domain(url: str) -> str:
    parts = urlsplit(url)
    host = (parts.netloc or "unknown").lower()
    if host.startswith("www."):
        host = host[4:]
    return host or "unknown"


def _publisher_key(item: ContentItem) -> str:
    if item.source == "reddit":
        subreddit = str(item.metadata_json.get("subreddit", "")).strip()
        return f"reddit:{subreddit or 'unknown'}"
    if item.source == "youtube":
        channel_id = str(item.metadata_json.get("channel_id", "")).strip()
        return f"youtube:{channel_id or 'unknown'}"
    if item.source == "twitter":
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


def _interest_overlap_score(item: ContentItem, user: User) -> float:
    interests = [interest.lower() for interest in user.interests]
    if not interests:
        return 0.5

    haystack = " ".join(
        filter(
            None,
            [
                item.title or "",
                item.body_text or "",
                item.author or "",
                str(item.metadata_json.get("subreddit", "")),
                str(item.metadata_json.get("feed_url", "")),
            ],
        )
    ).lower()

    matches = sum(1 for interest in interests if interest.lower() in haystack)
    if matches == 0:
        return 0.0
    return min(1.0, matches / min(len(interests), 3))


def compute_rank(item: ContentItem, user: User) -> float:
    """
    Composite rank score for `item` relative to `user`.

    Weights (tune based on early user feedback):
      quality_score      0.4  — depth and value
      authenticity_score 0.3  — real practitioner voice
      anxiety_score      0.3  — calm framing (higher = less anxious)
    """
    q = item.quality_score or 0.0
    a = item.authenticity_score or 0.0
    z = item.anxiety_score or 0.0
    r = _interest_overlap_score(item, user)
    if user.interests and r == 0.0:
        return round(q * 0.25 + a * 0.2 + z * 0.15, 4)
    return round(q * 0.3 + a * 0.2 + z * 0.15 + r * 0.35, 4)


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

    min_relevance = 0.1 if user.interests else 0.0
    filtered_items = [
        item for item in items
        if _interest_overlap_score(item, user) >= min_relevance
    ]
    candidate_items = filtered_items or items

    scored_items = sorted(candidate_items, key=lambda i: compute_rank(i, user), reverse=True)
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
