from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def observe(self, market_data: Dict[str, Any]) -> None:
        """Process incoming data"""
        pass

    @abstractmethod
    def evaluate(self, symbol: str) -> Dict[str, Any]:
        """Return agent's perspective and confidence on a symbol"""
        pass

class SectorIntelligenceAgent(BaseAgent):
    def __init__(self):
        super().__init__("SectorIntelligence")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.7, "thesis": "Sector rotation showing relative strength"}

class LiquidityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Liquidity")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.9, "thesis": "Order book depth supports execution"}

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("Risk")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.8, "thesis": "Volatility within acceptable parameters"}
