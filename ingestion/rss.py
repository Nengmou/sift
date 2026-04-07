"""RSS/Atom feed connector using feedparser."""
import asyncio
import hashlib
from email.utils import parsedate_to_datetime

import feedparser
import httpx

from ingestion.base import BaseConnector, RawItem, Source
from ingestion.og_image import fetch_og_image


class RSSConnector(BaseConnector):
    def __init__(self, feed_urls: list[str]):
        self.feed_urls = feed_urls

    async def fetch(self, **kwargs) -> list[RawItem]:
        """Parse all configured feed URLs and return normalized items."""
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(None, self._parse_feed, url)
            for url in self.feed_urls
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        items: list[RawItem] = []
        seen: set[str] = set()
        for result in results:
            if isinstance(result, list):
                for item in result:
                    if item.source_id not in seen:
                        seen.add(item.source_id)
                        items.append(item)

        # Fetch og:image for items that don't have a thumbnail yet
        needs_og = [i for i in items if not i.metadata.get("thumbnail_url") and i.url]
        if needs_og:
            async with httpx.AsyncClient(timeout=10) as client:
                og_tasks = [fetch_og_image(client, item.url) for item in needs_og]
                og_results = await asyncio.gather(*og_tasks, return_exceptions=True)
                for item, og_url in zip(needs_og, og_results, strict=True):
                    if isinstance(og_url, str):
                        item.metadata["thumbnail_url"] = og_url

        return items

    def _parse_feed(self, url: str) -> list[RawItem]:
        feed = feedparser.parse(url)
        items = []
        for entry in feed.entries:
            link = entry.get("link", "")
            source_id = entry.get("id") or hashlib.md5(link.encode()).hexdigest()

            published_at = None
            if entry.get("published"):
                try:
                    published_at = parsedate_to_datetime(entry.published)
                except Exception:
                    pass

            body = entry.get("summary") or entry.get("content", [{}])[0].get("value")

            # Extract thumbnail from feed media tags
            thumbnail_url = None
            media_thumbs = entry.get("media_thumbnail", [])
            if media_thumbs:
                thumbnail_url = media_thumbs[0].get("url")
            if not thumbnail_url:
                for mc in entry.get("media_content", []):
                    if mc.get("medium") == "image" or mc.get("type", "").startswith("image"):
                        thumbnail_url = mc.get("url")
                        break
            if not thumbnail_url:
                for link_entry in entry.get("links", []):
                    if link_entry.get("type", "").startswith("image"):
                        thumbnail_url = link_entry.get("href")
                        break

            items.append(RawItem(
                source=Source.RSS,
                source_id=source_id,
                url=link,
                title=entry.get("title"),
                author=entry.get("author"),
                body_text=body,
                published_at=published_at,
                content_type="article",
                metadata={"feed_url": url, "thumbnail_url": thumbnail_url},
            ))
        return items
