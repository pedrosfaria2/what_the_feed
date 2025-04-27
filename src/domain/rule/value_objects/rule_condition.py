from dataclasses import dataclass
from typing import Any, Dict

from src.seedwork.domain.base import ValueObject
from src.domain.rule.enums.logic_operator import LogicOperator
from src.domain.rule.enums.comparison_operator import ComparisonOperator


@dataclass(frozen=True)
class RuleCondition(ValueObject):
    """Value object representing a condition for applying rules."""

    field: str
    operator: ComparisonOperator
    value: Any
    logic: LogicOperator = LogicOperator.AND

    def evaluate(self, item: Dict[str, Any]) -> bool:
        """Evaluate this condition against an item."""
        if self.field not in item:
            return False

        field_value = item[self.field]

        if self.operator == ComparisonOperator.EQUALS:
            return field_value == self.value
        elif self.operator == ComparisonOperator.NOT_EQUALS:
            return field_value != self.value
        elif self.operator == ComparisonOperator.CONTAINS:
            return self.value in field_value
        elif self.operator == ComparisonOperator.NOT_CONTAINS:
            return self.value not in field_value
        elif self.operator == ComparisonOperator.GREATER_THAN:
            return field_value > self.value
        elif self.operator == ComparisonOperator.LESS_THAN:
            return field_value < self.value
        elif self.operator == ComparisonOperator.REGEX:
            import re

            pattern = re.compile(self.value)
            return bool(pattern.search(str(field_value)))

        return False
