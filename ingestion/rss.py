"""RSS/Atom feed connector using feedparser."""
import asyncio
import datetime
import hashlib
from email.utils import parsedate_to_datetime

import feedparser

from ingestion.base import BaseConnector, RawItem


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

            items.append(RawItem(
                source="rss",
                source_id=source_id,
                url=link,
                title=entry.get("title"),
                author=entry.get("author"),
                body_text=body,
                published_at=published_at,
                content_type="article",
                metadata={"feed_url": url},
            ))
        return items
