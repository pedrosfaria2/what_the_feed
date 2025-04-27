from enum import Enum


class RuleType(Enum):
    FILTER = "filter"
    TRANSFORM = "transform"
    TAG = "tag"
    SORT = "sort"
    GROUP = "group"
