"""Combines LLM scores into a composite rank for a given user."""
from db.models import ContentItem, User


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


def rank_items_for_user(
    items: list[ContentItem],
    user: User,
    max_per_source: int = 3,
    max_per_content_type: int = 8,
) -> list[ContentItem]:
    """
    Return items sorted by composite rank, with source diversity enforced.
    At most `max_per_source` items from the same source in the final list.
    """
    available_sources = _available_source_count(items)
    effective_max_per_source = max_per_source
    if available_sources <= 1:
        effective_max_per_source = 20
    elif available_sources == 2:
        effective_max_per_source = max(max_per_source, 10)

    min_relevance = 0.1 if user.interests else 0.0
    filtered_items = [
        item for item in items
        if _interest_overlap_score(item, user) >= min_relevance
    ]
    candidate_items = filtered_items or items

    sorted_items = sorted(candidate_items, key=lambda i: compute_rank(i, user), reverse=True)

    source_counts: dict[str, int] = {}
    content_type_counts: dict[str, int] = {}
    ranked: list[ContentItem] = []
    for item in sorted_items:
        source_count = source_counts.get(item.source, 0)
        content_type = item.content_type or "unknown"
        type_count = content_type_counts.get(content_type, 0)
        if source_count < effective_max_per_source and type_count < max_per_content_type:
            ranked.append(item)
            source_counts[item.source] = source_count + 1
            content_type_counts[content_type] = type_count + 1

    return ranked
