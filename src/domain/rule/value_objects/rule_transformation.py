from dataclasses import dataclass
from typing import Any, Dict, Optional, Callable

from src.domain.rule.enums.transformation_type import TransformationType
from src.seedwork.domain.base import ValueObject


@dataclass(frozen=True)
class RuleTransformation(ValueObject):
    """Value object representing a transformation to apply to feed items."""

    field: str
    type: TransformationType
    value: Any
    custom_function: Optional[Callable[[Any], Any]] = None

    def apply(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Apply this transformation to an item."""
        result = item.copy()

        if self.field not in result and self.type not in [
            TransformationType.APPEND,
            TransformationType.CUSTOM,
        ]:
            return result

        if self.type == TransformationType.REPLACE:
            result[self.field] = self.value
        elif self.type == TransformationType.APPEND:
            if self.field in result:
                result[self.field] = str(result[self.field]) + str(self.value)
            else:
                result[self.field] = self.value
        elif self.type == TransformationType.PREPEND:
            result[self.field] = str(self.value) + str(result[self.field])
        elif self.type == TransformationType.REMOVE:
            if self.field in result:
                del result[self.field]
        elif self.type == TransformationType.CUSTOM and self.custom_function:
            if self.field in result:
                result[self.field] = self.custom_function(result[self.field])

        return result
