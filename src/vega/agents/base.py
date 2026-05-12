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
        return {"confidence": 0.7, "thesis": "Sector showing structural relative strength and momentum breadth."}

class VolumeAgent(BaseAgent):
    def __init__(self):
        super().__init__("Volume")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.85, "thesis": "RVOL > 2.0 with positive delta confirming accumulation."}

class LiquidityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Liquidity")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.9, "thesis": "Thick liquidity zones present, absorption of selling pressure."}

class OptionsGammaAgent(BaseAgent):
    def __init__(self):
        super().__init__("OptionsGamma")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.75, "thesis": "Dealer positioning indicates long gamma, suppressing volatility expansion."}

class BreadthAgent(BaseAgent):
    def __init__(self):
        super().__init__("Breadth")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.65, "thesis": "Participation intensity is broadening across market caps."}

class RiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("Risk")

    def observe(self, market_data: Dict[str, Any]):
        pass

    def evaluate(self, symbol: str) -> Dict[str, Any]:
        return {"confidence": 0.8, "thesis": "Correlation regime stable, execution risk within defined limits."}
