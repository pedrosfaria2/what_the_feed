from abc import ABC
from dataclasses import dataclass
from typing import Any, Dict, Optional
import uuid


class Entity(ABC):
    """Base class for all entities with identity"""

    id: str

    def __init__(self, entity_id: Optional[str] = None):
        self.id = entity_id or str(uuid.uuid4())

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)


@dataclass(frozen=True)
class ValueObject:
    """Base class for all value objects"""

    def __post_init__(self):
        self._validate()

    def _validate(self):
        """Validate the value object`s invariants"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert the value object to a dictionary."""
        return {
            k: v for k, v in self.__dict__.items() if not k.startswith("_")
        }
