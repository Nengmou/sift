import asyncio

import pytest

from scoring import llm


def test_score_item_raises_without_api_key(monkeypatch):
    from ingestion.base import RawItem

    item = RawItem(
        source="rss",
        source_id="3",
        url="https://example.com/fallback",
        title="Calm practical guide",
        body_text="How I built this in production.",
    )

    monkeypatch.setattr(llm.settings, "openrouter_api_key", "")

    with pytest.raises(RuntimeError, match="No OpenRouter key configured"):
        asyncio.run(llm.score_item(item))
