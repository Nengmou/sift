"""Combines LLM scores into a composite rank for a given user."""
from db.models import ContentItem, User


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
    return round(q * 0.4 + a * 0.3 + z * 0.3, 4)


def rank_items_for_user(
    items: list[ContentItem],
    user: User,
    max_per_source: int = 3,
) -> list[ContentItem]:
    """
    Return items sorted by composite rank, with source diversity enforced.
    At most `max_per_source` items from the same source in the final list.
    """
    sorted_items = sorted(items, key=lambda i: compute_rank(i, user), reverse=True)

    source_counts: dict[str, int] = {}
    ranked: list[ContentItem] = []
    for item in sorted_items:
        count = source_counts.get(item.source, 0)
        if count < max_per_source:
            ranked.append(item)
            source_counts[item.source] = count + 1

    return ranked
