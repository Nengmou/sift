from types import SimpleNamespace

from scoring.ranker import compute_rank, rank_items_for_user


def make_user(*interests: str):
    return SimpleNamespace(interests=list(interests))


def make_item(
    source: str,
    title: str,
    *,
    url: str | None = None,
    quality: float = 0.8,
    authenticity: float = 0.8,
    calmness: float = 0.8,
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
        calmness_score=calmness,
        content_type=content_type,
    )


def test_diversity_cap_per_platform():
    user = make_user()
    items = [
        make_item(
            "rss", f"rss {i}",
            url=f"https://rss{i}.example.com/post",
        )
        for i in range(6)
    ] + [
        make_item(
            "reddit", f"reddit {i}",
            metadata_json={"subreddit": f"sub{i}"},
        )
        for i in range(3)
    ] + [
        make_item(
            "youtube", f"youtube {i}",
            metadata_json={"channel_id": f"chan{i}"},
            content_type="video",
        )
        for i in range(3)
    ]

    ranked = rank_items_for_user(
        items, user, max_per_platform=3, target_min_items=1,
    )

    assert sum(1 for item in ranked if item.source == "rss") <= 3
    assert sum(1 for item in ranked if item.source == "reddit") <= 3
    assert sum(1 for item in ranked if item.source == "youtube") <= 3


def test_diversity_cap_per_publisher():
    user = make_user()
    items = [
        make_item(
            "rss", f"hf {i}",
            url=f"https://huggingface.co/blog/{i}",
        )
        for i in range(6)
    ] + [
        make_item("rss", "other", url="https://simonwillison.net/post")
    ]

    ranked = rank_items_for_user(
        items, user, max_per_publisher=2, target_min_items=1,
    )

    hf_items = [item for item in ranked if "huggingface.co" in item.url]
    assert len(hf_items) <= 2


def test_interest_overlap_zero_returns_low_rank():
    user = make_user("AI agents & automation")
    off_topic = make_item(
        "rss", "Gardening tips",
        body_text="Tomatoes and soil health.",
    )
    on_topic = make_item(
        "rss", "AI agents in production",
        body_text="Agent orchestration.",
        metadata_json={
            "tags": [{"tag": "AI agents", "relevance": 1.0}],
        },
    )

    assert compute_rank(off_topic, user) < compute_rank(on_topic, user)


def test_tagged_item_with_matching_interest_scores_above_zero():
    user = make_user("AI agents & automation")
    item = make_item(
        "rss", "Building better AI workflows",
        body_text="Agent evaluation patterns.",
        metadata_json={
            "tags": [{"tag": "AI agents", "relevance": 0.8}],
        },
    )

    assert compute_rank(item, user) > 0.0


def test_no_interests_returns_full_quality_composite():
    user = make_user()
    item = make_item("rss", "Anything", quality=0.8, authenticity=0.8, calmness=0.8)

    # _relevance_score returns 1.0 for users with no interests
    # compute_rank = 1.0 * (0.5*0.8 + 0.3*0.8 + 0.2*0.8) = 0.8
    assert compute_rank(item, user) == 0.8


def test_rank_items_falls_back_to_all_when_filtered_pool_empty():
    user = make_user("AI agents & automation")
    items = [
        make_item(
            "rss", "Gardening tips",
            body_text="Tomatoes and soil health.",
        ),
        make_item(
            "reddit", "Cooking thread",
            metadata_json={"subreddit": "recipes"},
        ),
    ]

    ranked = rank_items_for_user(items, user)

    assert len(ranked) > 0


def test_high_authenticity_calm_item_survives_as_exploration():
    user = make_user("AI agents & automation")
    items = [
        make_item(
            "rss",
            "Engineering excellence from NASA",
            body_text="A calm, practical set of lessons learned.",
            quality=0.8,
            authenticity=0.9,
            calmness=0.9,
        ),
        make_item(
            "rss",
            "Gardening tips",
            body_text="Tomatoes and soil health.",
            quality=0.6,
            authenticity=0.4,
            calmness=0.7,
        ),
    ]

    ranked = rank_items_for_user(items, user, target_min_items=1)

    assert any(
        item.title == "Engineering excellence from NASA"
        for item in ranked
    )


def test_news_path_drops_authenticity_penalty():
    """News items use quality+calmness only; low authenticity should not hurt them."""
    user = make_user()
    news_item = make_item(
        "rss", "OpenAI release",
        quality=0.8, authenticity=0.1, calmness=0.9,
        metadata_json={"kind": "news"},
    )
    authentic_item = make_item(
        "rss", "Practitioner post",
        quality=0.8, authenticity=0.1, calmness=0.9,
        metadata_json={"kind": "authentic"},
    )
    # news = 1.0 * (0.6*0.8 + 0.4*0.9) = 0.84
    # authentic = 1.0 * (0.5*0.1 + 0.3*0.9 + 0.2*0.8) = 0.48
    assert compute_rank(news_item, user) == 0.84
    assert compute_rank(authentic_item, user) == 0.48
    assert compute_rank(news_item, user) > compute_rank(authentic_item, user)


def test_missing_kind_defaults_to_authentic_formula():
    """Items without metadata_json['kind'] use the authentic path (backwards compat)."""
    user = make_user()
    item = make_item("rss", "Untagged", quality=0.8, authenticity=0.8, calmness=0.8)
    assert compute_rank(item, user) == 0.8


def _quota_items(news_count: int, authentic_count: int):
    news = [
        make_item(
            "rss", f"news {i}",
            url=f"https://news{i}.example.com/post",
            metadata_json={"kind": "news"},
            content_type="article",
        )
        for i in range(news_count)
    ]
    authentic = [
        make_item(
            "reddit", f"authentic {i}",
            metadata_json={"kind": "authentic", "subreddit": f"sub{i}"},
            content_type="post",
        )
        for i in range(authentic_count)
    ]
    return news + authentic


def test_target_size_enforces_20_80_quota():
    user = make_user()
    items = _quota_items(news_count=10, authentic_count=10)
    ranked = rank_items_for_user(items, user, target_size=5)
    assert len(ranked) == 5
    assert sum(1 for i in ranked if i.metadata_json.get("kind") == "news") == 1
    assert sum(1 for i in ranked if i.metadata_json.get("kind") == "authentic") == 4


def test_target_size_backfills_when_news_is_empty():
    user = make_user()
    items = _quota_items(news_count=0, authentic_count=10)
    ranked = rank_items_for_user(items, user, target_size=5)
    assert len(ranked) == 5
    assert all(i.metadata_json.get("kind") == "authentic" for i in ranked)


def test_target_size_backfills_when_authentic_is_short():
    user = make_user()
    items = _quota_items(news_count=10, authentic_count=2)
    ranked = rank_items_for_user(items, user, target_size=5)
    assert len(ranked) == 5
    news_count = sum(1 for i in ranked if i.metadata_json.get("kind") == "news")
    authentic_count = sum(1 for i in ranked if i.metadata_json.get("kind") == "authentic")
    assert news_count == 3
    assert authentic_count == 2


def test_target_size_none_returns_full_ranked_list():
    """Without target_size, behavior is unchanged — no quota applied, no trim."""
    user = make_user()
    items = _quota_items(news_count=10, authentic_count=10)
    ranked = rank_items_for_user(items, user)
    # diversity caps may trim, but the quota must NOT kick in
    assert len(ranked) > 5


def test_adaptive_relaxation_fills_feed_with_default_target():
    user = make_user()
    items = [
        make_item(
            "rss", f"rss {i}",
            url=f"https://rss{i}.example.com/post",
        )
        for i in range(5)
    ] + [
        make_item(
            "reddit", f"reddit {i}",
            metadata_json={"subreddit": f"sub{i}"},
        )
        for i in range(5)
    ]

    ranked = rank_items_for_user(items, user)

    assert len(ranked) >= 8
