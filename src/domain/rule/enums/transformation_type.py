from enum import Enum


class TransformationType(Enum):
    REPLACE = "replace"
    APPEND = "append"
    PREPEND = "prepend"
    REMOVE = "remove"
    CUSTOM = "custom"
