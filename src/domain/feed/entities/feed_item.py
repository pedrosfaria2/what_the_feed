from typing import Optional, List

from src.seedwork.domain.base import Entity
from datetime import datetime


class FeedItem(Entity):
    """Entity representing an individual item from a feed."""

    def __init__(
        self,
        title: str,
        content: str,
        link: str,
        published_date: datetime,
        feed_id: Optional[str] = None,
        author: Optional[str] = None,
        feed_source_id: Optional[str] = None,
        guid: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        super().__init__(feed_id)
        self.title = title
        self.content = content
        self.link = link
        self.published_date = published_date
        self.author = author
        self.feed_source_id = feed_source_id
        self.guid = guid
        self.tags = tags

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
