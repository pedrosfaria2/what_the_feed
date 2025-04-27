from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.feed.entities.feed_item import FeedItem
from src.domain.mixer.entities.mixer import Mixer


class MixerRepository(ABC):
    """Repository interface for Mixer entities."""

    @abstractmethod
    def add(self, mixer: Mixer) -> None:
        """Add a new mixer to the repository."""
        pass

    @abstractmethod
    def get_by_id(self, mixer_id: str) -> Optional[Mixer]:
        """Get a mixer by its ID."""
        pass

    @abstractmethod
    def get_all(self, owner_id: Optional[str] = None) -> List[Mixer]:
        """Get all mixers, optionally filtered by owner."""
        pass

    @abstractmethod
    def update(self, mixer: Mixer) -> None:
        """Update an existing mixer."""
        pass

    @abstractmethod
    def delete(self, mixer_id: str) -> None:
        """Delete a mixer by its ID."""
        pass

    @abstractmethod
    def generate_mixed_feed(self, mixer_id: str) -> List[FeedItem]:
        """Generate a mixed feed by applying rules to feed items."""
        pass
