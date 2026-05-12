from dataclasses import dataclass
from enum import Enum, auto
import logging

logger = logging.getLogger("vega.intelligence.architecture")

class CognitionLevel(Enum):
    LAYER_1_OBSERVATION = auto()   # Cheap, continuous
    LAYER_2_REASONING = auto()     # Lightweight, conditional
    LAYER_3_STRATEGIC = auto()     # Expensive, high-value only

@dataclass
class TokenBudget:
    daily_limit: int = 1000000
    used: int = 0

    def can_afford(self, estimated_cost: int) -> bool:
        return (self.used + estimated_cost) <= self.daily_limit

    def consume(self, amount: int):
        self.used += amount

class CognitiveRouter:
    """Routes intelligence requests to the appropriate model based on value and cost."""
    def __init__(self):
        self.budget = TokenBudget()

    def route(self, context_value: float, required_level: CognitionLevel):
        if required_level == CognitionLevel.LAYER_1_OBSERVATION:
            return "cheap-model-fast"

        elif required_level == CognitionLevel.LAYER_2_REASONING:
            if context_value > 0.5:
                return "medium-model-reasoning"
            return "cheap-model-fast"

        elif required_level == CognitionLevel.LAYER_3_STRATEGIC:
            if context_value > 0.85 and self.budget.can_afford(5000):
                self.budget.consume(5000)
                logger.info("Activating expensive strategic cognition (Layer 3)")
                return "expensive-model-strategic"
            else:
                logger.warning("Strategic cognition requested but context value too low or budget exceeded")
                return "medium-model-reasoning"

        return "cheap-model-fast"
