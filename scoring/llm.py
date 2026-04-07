"""
LLM-based scoring via OpenRouter → Gemini Flash.
Scores each item on three dimensions (0.0–1.0):
  quality_score      — informational depth, sourcing, originality
  authenticity_score — personal voice, lived experience vs. performance
  calmness_score     — 1.0 = calm/constructive; 0.0 = stress-inducing/outrage bait
"""
import json
import logging
import re

import httpx

from config.settings import get_settings
from config.sources import TAG_VOCABULARY, TAG_VOCABULARY_SET
from ingestion.base import RawItem, Source

logger = logging.getLogger(__name__)
settings = get_settings()

_TAG_LIST = ", ".join(TAG_VOCABULARY)

SCORE_PROMPT = """You are a content quality evaluator for a calm, substance-focused content platform.

Score the following content on three dimensions, each as a float between 0.0 and 1.0:

1. quality: Informational depth, credible sourcing, practical value, originality.
   0 = shallow/clickbait, 1 = deep/well-sourced/original.

2. authenticity: Genuine personal experience or expertise vs. performative/engagement-bait.
   0 = repackaged hot takes, 1 = clear practitioner voice sharing real experience.

3. calmness: Emotional tone for the reader.
   0 = highly anxiety-inducing (urgency, doom, outrage, FOMO).
   1 = calm, constructive, informative without stress.

4. tags: Pick the TOP 3 most relevant tags ONLY from this list (maximum 3, minimum 0):
   {tag_list}
   Base your tags on what is explicitly stated in the title and body.
   Relevance: 1.0=main topic, 0.5=clearly covered, 0.2=briefly mentioned.
   Return [] if nothing matches.

Respond with ONLY valid JSON — no markdown, no explanation:
{{"quality": float, "authenticity": float, "calmness": float, "tags": [{{"tag": "tag name", "relevance": float}}], "why_this": "1-2 sentence user-facing summary"}}

Content to evaluate:
Source: {source}
Title: {title}
Body (first 500 chars): {body}
/no_think
"""

# Heuristic fallback used when no OpenRouter key is configured
_POSITIVE_SIGNALS = [
    "tutorial", "benchmark", "guide", "walkthrough", "lessons learned",
    "postmortem", "evaluation", "case study", "implementation", "how i",
]
_ANXIETY_SIGNALS = [
    "you are falling behind", "doom", "outrage", "must use now",
    "urgent", "panic", "threat", "replace everyone", "AI will replace",
]
_AUTHENTIC_SIGNALS = ["i built", "we built", "in production", "we shipped", "my experience"]


def _build_summary(item: RawItem) -> str:
    source_text = item.body_text or item.title or "Useful new content from your tracked sources."
    summary = re.sub(r"\s+", " ", source_text).strip()
    if not summary:
        summary = "Useful new content from your tracked sources."
    return summary[:220]


def _fallback_scores(item: RawItem) -> dict[str, float]:
    """Heuristic scoring when OpenRouter is unavailable."""
    text = f"{item.title or ''} {item.body_text or ''}".lower()
    quality = 0.55 + 0.06 * sum(1 for s in _POSITIVE_SIGNALS if s in text)
    authenticity = 0.5 + 0.10 * sum(1 for s in _AUTHENTIC_SIGNALS if s in text)
    calmness = 0.7 - 0.12 * sum(1 for s in _ANXIETY_SIGNALS if s in text)
    if item.source == Source.RSS:
        authenticity += 0.05
    if item.source == Source.HN:
        quality += 0.05
    return {
        "quality_score": float(max(0.0, min(1.0, quality))),
        "authenticity_score": float(max(0.0, min(1.0, authenticity))),
        "calmness_score": float(max(0.0, min(1.0, calmness))),
        "tags": [],
        "why_this": _build_summary(item),
    }


async def score_item(item: RawItem) -> dict[str, float]:
    """
    Score a RawItem. Falls back to heuristics if no OpenRouter key is set.
    Returns: {"quality_score": float, "authenticity_score": float, "calmness_score": float, "why_this": str}
    """
    if not settings.has_openrouter:
        logger.debug("No OpenRouter key — using fallback scores for %s", item.source_id)
        return _fallback_scores(item)

    prompt = SCORE_PROMPT.format(
        tag_list=_TAG_LIST,
        source=item.source,
        title=item.title or "(no title)",
        body=(item.body_text or "")[:500],
    )

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                f"{settings.openrouter_base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.openrouter_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 1024,
                },
            )
            resp.raise_for_status()

        content = resp.json()["choices"][0]["message"]["content"].strip()
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()
        content = re.sub(r":\s*(\d+)-(\d+)", r": \1.\2", content)  # fix 0-5 → 0.5
        parsed = json.loads(content)
        raw_tags = parsed.get("tags", [])
        seen: set[str] = set()
        validated_tags = []
        for t in raw_tags:
            if isinstance(t, dict) and t.get("tag") in TAG_VOCABULARY_SET and t["tag"] not in seen:
                seen.add(t["tag"])
                validated_tags.append({"tag": t["tag"], "relevance": float(max(0.0, min(1.0, t["relevance"])))})

        return {
            "quality_score": float(max(0.0, min(1.0, parsed["quality"]))),
            "authenticity_score": float(max(0.0, min(1.0, parsed["authenticity"]))),
            "calmness_score": float(max(0.0, min(1.0, parsed["calmness"]))),
            "tags": validated_tags,
            "why_this": str(parsed.get("why_this") or _build_summary(item)),
        }
    except (httpx.HTTPError, json.JSONDecodeError, KeyError, TypeError) as e:
        logger.warning("LLM scoring failed for %s: %s — using fallback", item.source_id, e)
        return _fallback_scores(item)
