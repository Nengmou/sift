"""
Backfill script: classify tags for already-scored items missing metadata_json["tags"].
Does NOT re-score quality/authenticity/calmness. Safe to re-run.
Run: python -m scripts.retag
"""
import asyncio
import json
import logging
import re

import httpx

from config.settings import get_settings
from config.sources import TAG_VOCABULARY, TAG_VOCABULARY_SET
from db.models import ContentItem
from db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = get_settings()

BATCH_SIZE = 50

_TAG_LIST = ", ".join(TAG_VOCABULARY)

RETAG_PROMPT = """Pick the TOP 3 most relevant tags for this content from the list below. Maximum 3 tags, minimum 0.
Base your tags on what is explicitly stated in the title and body.

Tags: {tag_list}

Relevance score: 1.0=main topic, 0.5=clearly covered, 0.2=briefly mentioned.

Source: {source}
Title: {title}
Body: {body}

Respond with ONLY valid JSON: {{"tags": [{{"tag": "...", "relevance": float}}]}}
If nothing matches: {{"tags": []}}
/no_think
"""


async def _classify_tags(item: ContentItem, client: httpx.AsyncClient) -> list[dict]:
    prompt = RETAG_PROMPT.format(
        tag_list=_TAG_LIST,
        source=item.source,
        title=item.title or "(no title)",
        body=(item.body_text or "")[:500],
    )
    try:
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
        validated = []
        for t in raw_tags:
            if isinstance(t, dict) and t.get("tag") in TAG_VOCABULARY_SET and t["tag"] not in seen:
                seen.add(t["tag"])
                validated.append({"tag": t["tag"], "relevance": float(max(0.0, min(1.0, t["relevance"])))})
        return validated
    except (httpx.HTTPError, json.JSONDecodeError, KeyError, TypeError) as e:
        logger.warning("Tag classification failed for %s: %s", item.source_id, e)
        return []


async def run_retag() -> None:
    if not settings.has_openrouter:
        logger.error("No OpenRouter key configured — cannot retag. Set OPENROUTER_API_KEY.")
        return

    db = SessionLocal()
    try:
        # Items that are scored but have no tags in metadata_json
        candidates = (
            db.query(ContentItem)
            .filter(ContentItem.quality_score.isnot(None))
            .order_by(ContentItem.ingested_at.desc())
            .all()
        )
        # Filter in Python: no tags key or empty tags list
        untagged = [
            item for item in candidates
            if not (item.metadata_json or {}).get("tags")
        ]
        logger.info("Found %d scored items without tags", len(untagged))

        async with httpx.AsyncClient(timeout=30) as client:
            for i in range(0, len(untagged), BATCH_SIZE):
                batch = untagged[i : i + BATCH_SIZE]
                logger.info("Processing batch %d–%d", i + 1, i + len(batch))
                for item in batch:
                    tags = await _classify_tags(item, client)
                    item.metadata_json = {
                        **(item.metadata_json or {}),
                        "tags": tags,
                    }
                db.commit()
                logger.info("Committed batch %d–%d (%d items tagged)", i + 1, i + len(batch), len(batch))

        logger.info("Retag complete")
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(run_retag())
