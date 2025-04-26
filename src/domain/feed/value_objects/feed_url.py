import re
from dataclasses import dataclass
from src.seedwork.domain.base import ValueObject


@dataclass(frozen=True)
class FeedUrl(ValueObject):
    """Value Object representing a feed URL"""

    url: str

    def _validate(self):
        if not self.url:
            raise ValueError("Feed URL cannot be empty")

        url_pattern = re.compile(
            r"^(https?://)"  # http:// or https://
            r"([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+"  # domain
            r"[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?"  # domain
            r"(/[^/\s]+)*/?$"  # path
        )

        if not url_pattern.match(self.url):
            raise ValueError(f"Invalid feed URL format: {self.url}")
