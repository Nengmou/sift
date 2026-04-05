from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class RawItem:
    """Normalized item returned by any connector before DB persistence."""
    source: str           # matches SourceEnum: hn/rss/reddit/twitter/youtube
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
