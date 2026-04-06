import asyncio

from ingestion.base import RawItem
from scoring import llm


def test_fallback_scores_returns_valid_range():
    item = RawItem(
        source="rss",
        source_id="1",
        url="https://example.com/post",
        title="Tutorial and benchmark",
        body_text="A practical implementation guide and case study.",
    )

    scores = llm._fallback_scores(item)

    assert 0.0 <= scores["quality_score"] <= 1.0
    assert 0.0 <= scores["authenticity_score"] <= 1.0
    assert 0.0 <= scores["calmness_score"] <= 1.0


def test_fallback_calmness_penalizes_doom_keywords():
    item = RawItem(
        source="rss",
        source_id="2",
        url="https://example.com/doom",
        title="Urgent doom warning",
        body_text="AI will replace everyone. Panic now. You are falling behind.",
    )

    scores = llm._fallback_scores(item)

    assert scores["calmness_score"] < 0.5


def test_llm_skipped_without_api_key(monkeypatch):
    item = RawItem(
        source="rss",
        source_id="3",
        url="https://example.com/fallback",
        title="Calm practical guide",
        body_text="How I built this in production.",
    )

    monkeypatch.setattr(llm.settings, "openrouter_api_key", "")

    result = asyncio.run(llm.score_item(item))

    assert set(result) == {
        "quality_score",
        "authenticity_score",
        "calmness_score",
        "why_this",
    }
