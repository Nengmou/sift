"""
LLM-based scoring via OpenRouter → Gemini Flash.
Scores each item on three dimensions (0.0–1.0):
  quality_score      — informational depth, sourcing, originality
  authenticity_score — personal voice, lived experience vs. performance
  anxiety_score      — 1.0 = calm/constructive; 0.0 = stress-inducing/outrage bait
"""
import json
import logging

import httpx

from config.settings import get_settings
from ingestion.base import RawItem

logger = logging.getLogger(__name__)
settings = get_settings()

SCORE_PROMPT = """You are a content quality evaluator for a calm, substance-focused content platform.

Score the following content on three dimensions, each as a float between 0.0 and 1.0:

1. quality: Informational depth, credible sourcing, practical value, originality.
   0 = shallow/clickbait, 1 = deep/well-sourced/original.

2. authenticity: Genuine personal experience or expertise vs. performative/engagement-bait.
   0 = repackaged hot takes, 1 = clear practitioner voice sharing real experience.

3. anxiety: Emotional tone for the reader.
   0 = highly anxiety-inducing (urgency, doom, outrage, FOMO).
   1 = calm, constructive, informative without stress.

Respond with ONLY valid JSON — no markdown, no explanation:
{{"quality": float, "authenticity": float, "anxiety": float}}

Content to evaluate:
Source: {source}
Title: {title}
Body (first 500 chars): {body}
"""


async def score_item(item: RawItem) -> dict[str, float]:
    """
    Call OpenRouter to score a single RawItem.
    Returns: {"quality_score": float, "authenticity_score": float, "anxiety_score": float}
    """
    prompt = SCORE_PROMPT.format(
        source=item.source,
        title=item.title or "(no title)",
        body=(item.body_text or "")[:500],
    )

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
                "max_tokens": 100,
            },
        )
        resp.raise_for_status()

    content = resp.json()["choices"][0]["message"]["content"].strip()

    try:
        parsed = json.loads(content)
        return {
            "quality_score": float(max(0.0, min(1.0, parsed["quality"]))),
            "authenticity_score": float(max(0.0, min(1.0, parsed["authenticity"]))),
            "anxiety_score": float(max(0.0, min(1.0, parsed["anxiety"]))),
        }
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        logger.warning("Failed to parse LLM score response for %s: %s | raw: %s",
                       item.source_id, e, content)
        return {"quality_score": 0.5, "authenticity_score": 0.5, "anxiety_score": 0.5}
