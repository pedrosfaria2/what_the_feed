from datetime import datetime
from typing import Optional, List

from src.domain.feed.value_objects.feed_status import FeedStatus
from src.domain.feed.value_objects.feed_url import FeedUrl
from src.seedwork.domain.base import Entity
from src.domain.feed.entities.feed_item import FeedItem


class Feed(Entity):
    """Feed entity representing an RSS feed source"""

    def __init__(
        self,
        name: str,
        url: FeedUrl,
        feed_source_id: Optional[str] = None,
        description: Optional[str] = None,
        last_fetched: Optional[datetime] = None,
        status: FeedStatus = FeedStatus.ACTIVE,
    ):
        super().__init__(entity_id=feed_source_id)
        self.name = name
        self.url = url
        self.description = description
        self.last_fetched = last_fetched
        self.status = status
        self._items: List["FeedItem"] = []

    def add_item(self, item: "FeedItem"):
        self._items.append(item)

    def update_last_fetched(self):
        self.last_fetched = datetime.now()

    @property
    def items(self) -> List["FeedItem"]:
        return self._items.copy()

    def is_stale(self, max_age_minutes: int = 60) -> bool:
        if not self.last_fetched:
            return True

        age = datetime.now() - self.last_fetched
        return age.total_seconds() / 60 > max_age_minutes
