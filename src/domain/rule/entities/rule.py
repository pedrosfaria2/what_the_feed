from typing import Any, Dict, List, Optional

from src.domain.rule.enums.rule_type import RuleType
from src.domain.rule.value_objects.rule_condition import RuleCondition
from src.domain.rule.value_objects.rule_transformation import (
    RuleTransformation,
)
from src.seedwork.domain.base import Entity


class Rule(Entity):
    """Entity representing a transformation or filtering rule."""

    def __init__(
        self,
        name: str,
        rule_type: RuleType,
        id: Optional[str] = None,
        description: Optional[str] = None,
        conditions: Optional[List[RuleCondition]] = None,
        transformations: Optional[List[RuleTransformation]] = None,
        priority: int = 0,
    ):
        super().__init__(id)
        self.name = name
        self.rule_type = rule_type
        self.description = description
        self.conditions = conditions or []
        self.transformations = transformations or []
        self.priority = priority

    def add_condition(self, condition: RuleCondition) -> None:
        """Add a condition to this rule."""
        self.conditions.append(condition)

    def add_transformation(self, transformation: RuleTransformation) -> None:
        """Add a transformation to this rule."""
        self.transformations.append(transformation)

    def matches(self, item: Dict[str, Any]) -> bool:
        """Check if the item matches all conditions of this rule."""
        if not self.conditions:
            return True

        return all(condition.evaluate(item) for condition in self.conditions)

    def apply(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Apply all transformations of this rule to the item."""
        if not self.transformations:
            return item

        result = item.copy()
        for transformation in self.transformations:
            result = transformation.apply(result)

        return result
