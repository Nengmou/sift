from types import SimpleNamespace

from scoring.ranker import _interest_overlap_score, compute_rank, rank_items_for_user


def make_user(*interests: str):
    return SimpleNamespace(interests=list(interests))


def make_item(
    source: str,
    title: str,
    *,
    url: str | None = None,
    quality: float = 0.8,
    authenticity: float = 0.8,
    anxiety: float = 0.8,
    content_type: str = "article",
    author: str | None = None,
    body_text: str | None = None,
    metadata_json: dict | None = None,
):
    return SimpleNamespace(
        source=source,
        url=url or "https://example.com/post",
        title=title,
        body_text=body_text or "",
        author=author,
        metadata_json=metadata_json or {},
        quality_score=quality,
        authenticity_score=authenticity,
        anxiety_score=anxiety,
        content_type=content_type,
    )


def test_diversity_cap_per_platform():
    user = make_user()
    items = [
        make_item("rss", f"rss {i}", url=f"https://rss{i}.example.com/post")
        for i in range(6)
    ] + [
        make_item("reddit", f"reddit {i}", metadata_json={"subreddit": f"sub{i}"})
        for i in range(3)
    ] + [
        make_item("youtube", f"youtube {i}", metadata_json={"channel_id": f"chan{i}"}, content_type="video")
        for i in range(3)
    ]

    ranked = rank_items_for_user(items, user, max_per_platform=3, target_min_items=1)

    assert sum(1 for item in ranked if item.source == "rss") <= 3
    assert sum(1 for item in ranked if item.source == "reddit") <= 3
    assert sum(1 for item in ranked if item.source == "youtube") <= 3


def test_diversity_cap_per_publisher():
    user = make_user()
    items = [
        make_item("rss", f"hf {i}", url=f"https://huggingface.co/blog/{i}")
        for i in range(6)
    ] + [
        make_item("rss", "other", url="https://simonwillison.net/post")
    ]

    ranked = rank_items_for_user(items, user, max_per_publisher=2, target_min_items=1)

    hf_items = [item for item in ranked if "huggingface.co" in item.url]
    assert len(hf_items) <= 2


def test_interest_overlap_zero_returns_low_rank():
    user = make_user("AI agents")
    off_topic = make_item("rss", "Gardening tips", body_text="Tomatoes and soil health.")
    on_topic = make_item("rss", "AI agents in production", body_text="Agent orchestration.")

    assert compute_rank(off_topic, user) < compute_rank(on_topic, user)


def test_no_interests_returns_half():
    user = make_user()
    item = make_item("rss", "Anything")

    assert _interest_overlap_score(item, user) == 0.5


def test_rank_items_falls_back_to_all_when_filtered_pool_empty():
    user = make_user("AI agents")
    items = [
        make_item("rss", "Gardening tips", body_text="Tomatoes and soil health."),
        make_item("reddit", "Cooking thread", metadata_json={"subreddit": "recipes"}),
    ]

    ranked = rank_items_for_user(items, user)

    assert len(ranked) > 0


def test_adaptive_relaxation_fills_feed_with_default_target():
    user = make_user()
    items = [
        make_item("rss", f"rss {i}", url=f"https://rss{i}.example.com/post")
        for i in range(5)
    ] + [
        make_item("reddit", f"reddit {i}", metadata_json={"subreddit": f"sub{i}"})
        for i in range(5)
    ]

    ranked = rank_items_for_user(items, user)

    assert len(ranked) >= 8
