from typing import List, Optional

from src.domain.rule.entities.rule import Rule
from src.seedwork.domain.base import Entity
from src.domain.feed.entities.feed import Feed


class Mixer(Entity):
    """Entity representing a custom feed mixer"""

    def __init__(
        self,
        name: str,
        mixer_id: Optional[str] = None,
        description: Optional[str] = None,
        is_public: bool = True,
        output_format: str = "rss",
    ):
        super().__init__(mixer_id)
        self.name = name
        self.description = description
        self.is_public = is_public
        self.output_format = output_format
        self._feeds: List[Feed] = []
        self._rules: List["Rule"] = []

    def add_feed(self, feed: Feed) -> None:
        """Add a feed to this mixer."""
        if feed not in self._feeds:
            self._feeds.append(feed)

    def remove_feed(self, feed_id: str) -> None:
        """Remove a feed from this mixer."""
        self._feeds = [f for f in self._feeds if f.id != feed_id]

    def add_rule(self, rule: "Rule") -> None:
        """Add a rule to this mixer."""
        if rule not in self._rules:
            self._rules.append(rule)

    def remove_rule(self, rule_id: str) -> None:
        """Remove a rule from this mixer."""
        self._rules = [r for r in self._rules if r.id != rule_id]

    @property
    def feeds(self) -> List[Feed]:
        """Get all feeds for this mixer."""
        return self._feeds.copy()

    @property
    def rules(self) -> List["Rule"]:
        """Get all rules for this mixer."""
        return self._rules.copy()
