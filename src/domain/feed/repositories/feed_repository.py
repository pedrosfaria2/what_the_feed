from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.feed.entities.feed import Feed
from src.domain.feed.entities.feed_item import FeedItem


class FeedRepository(ABC):
    """Repository interface for Feed entities."""

    @abstractmethod
    def add(self, feed: Feed) -> None:
        """Add a new feed to the repository."""
        pass

    @abstractmethod
    def get_by_id(self, feed_id: str) -> Optional[Feed]:
        """Get a feed by its ID."""
        pass

    @abstractmethod
    def get_all(self) -> List[Feed]:
        """Get all feeds."""
        pass

    @abstractmethod
    def update(self, feed: Feed) -> None:
        """Update an existing feed."""
        pass

    @abstractmethod
    def delete(self, feed_id: str) -> None:
        """Delete a feed by its ID."""
        pass

    @abstractmethod
    def fetch_content(self, feed_id: str) -> List[FeedItem]:
        """Fetch and parse the content of a feed."""
        pass
