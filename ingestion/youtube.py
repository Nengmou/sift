"""
YouTube connector stub — uses YouTube Data API v3.
Add YOUTUBE_API_KEY to .env when ready to enable.
yt-dlp can be used to fetch transcripts for already-discovered video IDs.
"""
import datetime
import logging

import httpx

from ingestion.base import BaseConnector, RawItem, Source

BASE_URL = "https://www.googleapis.com/youtube/v3"
logger = logging.getLogger(__name__)


class YouTubeConnector(BaseConnector):
    def __init__(self, api_key: str, channel_ids: list[str] | None = None):
        self.api_key = api_key
        self.channel_ids = channel_ids or []

    async def fetch(self, max_results: int = 10, **kwargs) -> list[RawItem]:
        """
        Fetch recent videos from configured channels or handles.
        """
        if not self.channel_ids:
            return []

        items_by_id: dict[str, RawItem] = {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            for identifier in self.channel_ids:
                channel_id = await self._resolve_channel_id(client, identifier)
                if not channel_id:
                    logger.warning("YouTubeConnector: unable to resolve channel %s", identifier)
                    continue
                for item in await self._fetch_channel_videos(client, channel_id, max_results):
                    items_by_id[item.source_id] = item

        return sorted(
            items_by_id.values(),
            key=lambda item: item.published_at or datetime.datetime.min.replace(
                tzinfo=datetime.timezone.utc
            ),
            reverse=True,
        )

    async def _resolve_channel_id(
        self, client: httpx.AsyncClient, identifier: str
    ) -> str | None:
        if identifier.startswith("UC"):
            return identifier
        if not identifier.startswith("@"):
            return identifier

        resp = await client.get(
            f"{BASE_URL}/channels",
            params={
                "part": "id",
                "forHandle": identifier,
                "key": self.api_key,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        for item in data.get("items", []):
            channel_id = item.get("id")
            if channel_id:
                return channel_id
        return None

    async def _fetch_channel_videos(
        self, client: httpx.AsyncClient, channel_id: str, max_results: int
    ) -> list[RawItem]:
        params = {
            "part": "snippet",
            "channelId": channel_id,
            "maxResults": max_results,
            "order": "date",
            "type": "video",
            "key": self.api_key,
        }
        resp = await client.get(f"{BASE_URL}/search", params=params)
        resp.raise_for_status()
        data = resp.json()

        items = []
        for item in data.get("items", []):
            snippet = item.get("snippet", {})
            video_id = item.get("id", {}).get("videoId")
            if not video_id:
                continue

            published_at = None
            if snippet.get("publishedAt"):
                published_at = datetime.datetime.fromisoformat(
                    snippet["publishedAt"].replace("Z", "+00:00")
                )

            items.append(RawItem(
                source=Source.YOUTUBE,
                source_id=video_id,
                url=f"https://www.youtube.com/watch?v={video_id}",
                title=snippet.get("title"),
                author=snippet.get("channelTitle"),
                body_text=snippet.get("description"),
                published_at=published_at,
                content_type="video",
                metadata={"channel_id": channel_id, "thumbnail": snippet.get("thumbnails", {})},
            ))
        return items
