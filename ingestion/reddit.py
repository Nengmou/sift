"""Reddit connector — uses Reddit's public JSON API (no OAuth required for read-only)."""
import datetime

import httpx

from ingestion.base import BaseConnector, RawItem, Source

BASE_URL = "https://www.reddit.com"
HEADERS = {"User-Agent": "sift/0.1 (authentic content discovery)"}


class RedditConnector(BaseConnector):
    def __init__(self, subreddits: list[str]):
        self.subreddits = subreddits

    async def fetch(self, sort: str = "hot", limit: int = 25) -> list[RawItem]:
        """Fetch posts from each configured subreddit."""
        async with httpx.AsyncClient(headers=HEADERS, timeout=10) as client:
            all_items: list[RawItem] = []
            for subreddit in self.subreddits:
                url = f"{BASE_URL}/r/{subreddit}/{sort}.json?limit={limit}"
                try:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    data = resp.json()
                    for child in data.get("data", {}).get("children", []):
                        item = self._normalize(child["data"], subreddit)
                        if item:
                            all_items.append(item)
                except Exception:
                    continue
        return all_items

    def _normalize(self, post: dict, subreddit: str) -> RawItem | None:
        if post.get("stickied"):
            return None

        published_at = None
        if post.get("created_utc"):
            published_at = datetime.datetime.fromtimestamp(
                post["created_utc"], tz=datetime.timezone.utc
            )

        is_self = post.get("is_self", False)
        url = post.get("url", "")
        content_type = "post" if is_self else "article"

        return RawItem(
            source=Source.REDDIT,
            source_id=post["id"],
            url=url,
            title=post.get("title"),
            author=post.get("author"),
            body_text=post.get("selftext") if is_self else None,
            published_at=published_at,
            content_type=content_type,
            metadata={
                "subreddit": subreddit,
                "score": post.get("score", 0),
                "num_comments": post.get("num_comments", 0),
                "permalink": f"https://reddit.com{post.get('permalink', '')}",
            },
        )
