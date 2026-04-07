from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class Source(StrEnum):
    HN      = "hn"
    RSS     = "rss"
    REDDIT  = "reddit"
    TWITTER = "twitter"
    YOUTUBE = "youtube"


@dataclass
class RawItem:
    """Normalized item returned by any connector before DB persistence."""
    source: str           # Source enum value
    source_id: str        # unique identifier within that source
    url: str
    title: str | None = None
    author: str | None = None
    body_text: str | None = None
    published_at: datetime | None = None
    content_type: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseConnector(ABC):
    @abstractmethod
    async def fetch(self, **kwargs) -> list[RawItem]:
        """Fetch and normalize new items from the source."""
        ...
