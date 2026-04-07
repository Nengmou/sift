"""Hacker News connector — uses the official Firebase REST API (free, no auth)."""
import asyncio

import httpx

from ingestion.base import BaseConnector, RawItem, Source
from ingestion.og_image import fetch_og_image

BASE_URL = "https://hacker-news.firebaseio.com/v0"


class HNConnector(BaseConnector):
    async def fetch(self, story_type: str = "topstories", limit: int = 50) -> list[RawItem]:
        """
        Fetch stories from HN.
        story_type: topstories | newstories | beststories
        """
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(f"{BASE_URL}/{story_type}.json")
            resp.raise_for_status()
            ids = resp.json()[:limit]

            tasks = [self._fetch_item(client, item_id) for item_id in ids]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        items = []
        for r in results:
            if isinstance(r, RawItem):
                items.append(r)
        return items

    async def _fetch_item(self, client: httpx.AsyncClient, item_id: int) -> RawItem | None:
        resp = await client.get(f"{BASE_URL}/item/{item_id}.json")
        resp.raise_for_status()
        data = resp.json()
        if not data or data.get("type") != "story":
            return None

        import datetime
        published_at = None
        if data.get("time"):
            published_at = datetime.datetime.fromtimestamp(
                data["time"], tz=datetime.UTC
            )

        url = data.get("url") or f"https://news.ycombinator.com/item?id={data['id']}"

        # Fetch og:image for external links (skip HN self-posts)
        thumbnail_url = None
        if url and "news.ycombinator.com" not in url:
            thumbnail_url = await fetch_og_image(client, url)

        return RawItem(
            source=Source.HN,
            source_id=str(data["id"]),
            url=url,
            title=data.get("title"),
            author=data.get("by"),
            body_text=data.get("text"),
            published_at=published_at,
            content_type="article",
            metadata={
                "score": data.get("score", 0),
                "descendants": data.get("descendants", 0),
                "thumbnail_url": thumbnail_url,
            },
        )
