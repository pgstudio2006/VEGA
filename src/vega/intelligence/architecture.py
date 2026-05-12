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

import time

class CognitiveRouter:
    """Routes intelligence requests to the appropriate model based on value and cost.
       Implements semantic caching and cognition cooldowns to maximize alpha per token.
    """
    def __init__(self):
        self.budget = TokenBudget()
        self.semantic_cache = {}
        self.cooldowns = {}

    def check_cache(self, symbol: str, required_level: CognitionLevel) -> bool:
        cache_key = f"{symbol}_{required_level.name}"
        if cache_key in self.cooldowns:
            if time.time() - self.cooldowns[cache_key] < 60: # 60s cooldown
                return True
        return False

    def route(self, symbol: str, context_value: float, required_level: CognitionLevel):
        if self.check_cache(symbol, required_level):
            logger.debug(f"[{symbol}] Cognition cooldown active. Reusing cached reasoning.")
            return "cached-reasoning"

        cache_key = f"{symbol}_{required_level.name}"
        self.cooldowns[cache_key] = time.time()

        if required_level == CognitionLevel.LAYER_1_OBSERVATION:
            return "cheap-model-fast"

        elif required_level == CognitionLevel.LAYER_2_REASONING:
            if context_value > 0.5:
                return "medium-model-reasoning"
            return "cheap-model-fast"

        elif required_level == CognitionLevel.LAYER_3_STRATEGIC:
            if context_value > 0.85 and self.budget.can_afford(5000):
                self.budget.consume(5000)
                logger.info(f"[{symbol}] Activating expensive strategic cognition (Layer 3)")
                return "expensive-model-strategic"
            else:
                logger.warning(f"[{symbol}] Strategic cognition gated. Insufficient context value or budget.")
                return "medium-model-reasoning"

        return "cheap-model-fast"
