"""
YouTube connector stub — uses YouTube Data API v3.
Add YOUTUBE_API_KEY to .env when ready to enable.
yt-dlp can be used to fetch transcripts for already-discovered video IDs.
"""
import datetime

import httpx

from ingestion.base import BaseConnector, RawItem

BASE_URL = "https://www.googleapis.com/youtube/v3"


class YouTubeConnector(BaseConnector):
    def __init__(self, api_key: str, channel_ids: list[str] | None = None):
        self.api_key = api_key
        self.channel_ids = channel_ids or []

    async def fetch(self, max_results: int = 10, **kwargs) -> list[RawItem]:
        """
        Fetch recent videos from configured channels.
        TODO: implement YouTube Data API v3 search + transcript fetch via yt-dlp.
        """
        raise NotImplementedError(
            "YouTube connector not yet implemented. "
            "Add YOUTUBE_API_KEY to .env and implement _fetch_channel_videos."
        )

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
                source="youtube",
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
