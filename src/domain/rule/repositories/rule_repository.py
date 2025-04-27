from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.rule.entities.rule import Rule


class RuleRepository(ABC):
    """Repository interface for Rule entities."""

    @abstractmethod
    def add(self, rule: Rule) -> None:
        """Add a new rule to the repository."""
        pass

    @abstractmethod
    def get_by_id(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by its ID."""
        pass

    @abstractmethod
    def get_by_mixer_id(self, mixer_id: str) -> List[Rule]:
        """Get all rules for a mixer."""
        pass

    @abstractmethod
    def update(self, rule: Rule) -> None:
        """Update an existing rule."""
        pass

    @abstractmethod
    def delete(self, rule_id: str) -> None:
        """Delete a rule by its ID."""
        pass
