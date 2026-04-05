"""
Twitter/X connector stub — requires X API v2 Bearer token.
Add TWITTER_BEARER_TOKEN to .env when ready to enable.
"""
import datetime

import httpx

from ingestion.base import BaseConnector, RawItem

BASE_URL = "https://api.twitter.com/2"


class TwitterConnector(BaseConnector):
    def __init__(self, bearer_token: str):
        self.bearer_token = bearer_token

    async def fetch(self, query: str = "", max_results: int = 20) -> list[RawItem]:
        """
        Search recent tweets. Requires a curated query string, e.g.:
        "(from:karpathy OR from:simonw) -is:retweet lang:en"
        TODO: implement X API v2 /tweets/search/recent call.
        """
        raise NotImplementedError(
            "Twitter connector not yet implemented. "
            "Add TWITTER_BEARER_TOKEN to .env and implement _search_recent."
        )

    async def _search_recent(
        self, client: httpx.AsyncClient, query: str, max_results: int
    ) -> list[RawItem]:
        params = {
            "query": query,
            "max_results": max_results,
            "tweet.fields": "author_id,created_at,public_metrics,entities",
            "expansions": "author_id",
            "user.fields": "name,username",
        }
        resp = await client.get(
            f"{BASE_URL}/tweets/search/recent",
            params=params,
            headers={"Authorization": f"Bearer {self.bearer_token}"},
        )
        resp.raise_for_status()
        data = resp.json()

        users = {u["id"]: u for u in data.get("includes", {}).get("users", [])}
        items = []
        for tweet in data.get("data", []):
            author = users.get(tweet.get("author_id"), {})
            published_at = None
            if tweet.get("created_at"):
                published_at = datetime.datetime.fromisoformat(
                    tweet["created_at"].replace("Z", "+00:00")
                )
            items.append(RawItem(
                source="twitter",
                source_id=tweet["id"],
                url=f"https://twitter.com/i/web/status/{tweet['id']}",
                title=None,
                author=author.get("username"),
                body_text=tweet.get("text"),
                published_at=published_at,
                content_type="thread",
                metadata={"public_metrics": tweet.get("public_metrics", {})},
            ))
        return items
