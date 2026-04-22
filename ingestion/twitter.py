"""
Twitter/X connector stub — requires X API v2 Bearer token.
Add TWITTER_BEARER_TOKEN to .env when ready to enable.
"""
import datetime
from itertools import islice

import httpx

from config.sources import TWITTER_NEWS_ACCOUNTS_SET
from ingestion.base import BaseConnector, RawItem, Source

BASE_URL = "https://api.twitter.com/2"
MAX_USERNAMES_PER_QUERY = 20


class TwitterConnector(BaseConnector):
    def __init__(self, bearer_token: str, usernames: list[str] | None = None):
        self.bearer_token = bearer_token
        self.usernames = [username.lstrip("@") for username in (usernames or [])]

    async def fetch(self, query: str = "", max_results: int = 20) -> list[RawItem]:
        """
        Search recent tweets from configured accounts.
        Falls back to a caller-supplied query if usernames are not configured.
        """
        queries = []
        if self.usernames:
            for username_batch in _batched(self.usernames, MAX_USERNAMES_PER_QUERY):
                account_clause = " OR ".join(f"from:{username}" for username in username_batch)
                queries.append(f"({account_clause}) -is:retweet -is:reply lang:en")
        elif query:
            queries.append(query)
        else:
            return []

        items_by_id: dict[str, RawItem] = {}
        async with httpx.AsyncClient(timeout=30.0) as client:
            for search_query in queries:
                for item in await self._search_recent(client, search_query, max_results):
                    items_by_id[item.source_id] = item

        return sorted(
            items_by_id.values(),
            key=lambda item: item.published_at or datetime.datetime.min.replace(
                tzinfo=datetime.UTC
            ),
            reverse=True,
        )

    async def _search_recent(
        self, client: httpx.AsyncClient, query: str, max_results: int
    ) -> list[RawItem]:
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "author_id,created_at,public_metrics,entities,attachments",
            "expansions": "author_id,attachments.media_keys",
            "user.fields": "name,username",
            "media.fields": "preview_image_url,url,type",
        }
        resp = await client.get(
            f"{BASE_URL}/tweets/search/recent",
            params=params,
            headers={"Authorization": f"Bearer {self.bearer_token}"},
        )
        resp.raise_for_status()
        data = resp.json()

        includes = data.get("includes", {})
        users = {u["id"]: u for u in includes.get("users", [])}
        media_map = {m["media_key"]: m for m in includes.get("media", [])}

        items = []
        for tweet in data.get("data", []):
            author = users.get(tweet.get("author_id"), {})
            published_at = None
            if tweet.get("created_at"):
                published_at = datetime.datetime.fromisoformat(
                    tweet["created_at"].replace("Z", "+00:00")
                )

            # Extract first image from tweet media attachments
            thumbnail_url = None
            media_keys = tweet.get("attachments", {}).get("media_keys", [])
            for key in media_keys:
                media = media_map.get(key, {})
                thumbnail_url = media.get("preview_image_url") or media.get("url")
                if thumbnail_url:
                    break

            username = author.get("username")
            items.append(RawItem(
                source=Source.TWITTER,
                source_id=tweet["id"],
                url=f"https://twitter.com/i/web/status/{tweet['id']}",
                title=None,
                author=username,
                body_text=tweet.get("text"),
                published_at=published_at,
                content_type="thread",
                metadata={
                    "public_metrics": tweet.get("public_metrics", {}),
                    "thumbnail_url": thumbnail_url,
                    "kind": (
                        "news"
                        if username and username in TWITTER_NEWS_ACCOUNTS_SET
                        else "authentic"
                    ),
                },
            ))
        return items


def _batched(items: list[str], size: int):
    iterator = iter(items)
    while batch := list(islice(iterator, size)):
        yield batch
