from dataclasses import dataclass, field
from typing import Dict, Any, List
import logging

logger = logging.getLogger("vega.intelligence.market_structure")

@dataclass
class SectorData:
    relative_strength: float = 1.0
    participation_rate: float = 0.5
    trend_alignment: str = "NEUTRAL"

@dataclass
class MarketEcology:
    regime: str = "UNKNOWN"
    volatility_regime: str = "NORMAL"
    liquidity_regime: str = "ADEQUATE"
    correlation_regime: str = "MIXED"

    breadth_score: float = 0.5
    momentum_breadth: float = 0.5
    risk_on_off: str = "NEUTRAL"

    sector_rotation: Dict[str, SectorData] = field(default_factory=dict)

    def update(self, data: Dict[str, Any]):
        self.regime = data.get("regime", self.regime)
        self.volatility_regime = data.get("volatility_regime", self.volatility_regime)
        self.liquidity_regime = data.get("liquidity_regime", self.liquidity_regime)
        self.correlation_regime = data.get("correlation_regime", self.correlation_regime)
        self.breadth_score = data.get("breadth", self.breadth_score)
        self.momentum_breadth = data.get("momentum_breadth", self.momentum_breadth)
        self.risk_on_off = data.get("risk_on_off", self.risk_on_off)

        if "sectors" in data:
            for sector_name, sector_info in data["sectors"].items():
                self.sector_rotation[sector_name] = SectorData(**sector_info)

        logger.debug(f"Market Ecology Updated: {self.regime} | Vol: {self.volatility_regime} | Breadth: {self.breadth_score:.2f} | Risk: {self.risk_on_off}")

class MarketStructureEngine:
    def __init__(self):
        self.ecology = MarketEcology()

    def analyze_relative_strength(self, symbol: str, sector: str) -> float:
        # Evaluate how symbol performs relative to its sector
        sector_data = self.ecology.sector_rotation.get(sector, SectorData())
        # Placeholder for deep RS calculation
        rs_score = 1.0 + (sector_data.relative_strength - 1.0) * 0.5
        return rs_score

    def assess_market_stress(self) -> float:
        stress = 0.0
        if self.ecology.volatility_regime in ["HIGH", "EXPANDING"]:
            stress += 0.4
        if self.ecology.liquidity_regime in ["STRESSED", "VACUUM"]:
            stress += 0.4
        if self.ecology.breadth_score < 0.3:
            stress += 0.2
        return stress
