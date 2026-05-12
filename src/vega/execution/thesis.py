from dataclasses import dataclass, field
from typing import Dict, Any, List
import logging

logger = logging.getLogger("vega.execution.thesis")

@dataclass
class TradeThesis:
    symbol: str
    primary_catalyst: str = ""
    sector_context: str = ""
    volume_confirmation: str = ""
    liquidity_context: str = ""
    volatility_structure: str = ""
    breadth_support: str = ""

    archetype: str = "UNKNOWN" # e.g. BREAKOUT, MEAN_REVERSION, VOLATILITY_EXPANSION
    expected_holding_profile: str = "INTRADAY" # SWING, POSITION
    invalidation_criteria: List[str] = field(default_factory=list)
    confidence_score: float = 0.0

    def is_valid_for_execution(self) -> bool:
        """Requires high-confidence multi-factor alignment before execution."""
        if self.confidence_score < 0.8:
            return False

        required_factors = [
            self.volume_confirmation,
            self.liquidity_context,
            self.sector_context
        ]

        # Ensure core structural reasons are explicitly stated
        return all(len(factor) > 5 for factor in required_factors)

    def render_explainable(self) -> str:
        return (
            f"Thesis [{self.symbol}]: {self.primary_catalyst}. "
            f"Supported by volume ({self.volume_confirmation}) and liquidity ({self.liquidity_context}). "
            f"Context: {self.sector_context}."
        )

class ThesisEngine:
    def _determine_archetype(self, perspectives: Dict[str, Any]) -> str:
        # Simplistic heuristic for archetype determination based on agent narratives
        combined_text = " ".join([p.get("thesis", "") for p in perspectives.values()]).lower()
        if "breakout" in combined_text or "accumulation" in combined_text:
            return "BREAKOUT"
        if "mean reversion" in combined_text or "exhaustion" in combined_text:
            return "MEAN_REVERSION"
        if "volatility expansion" in combined_text:
            return "VOLATILITY_EXPANSION"
        return "MOMENTUM_CONTINUATION"

    def formulate_thesis(self, symbol: str, agent_perspectives: Dict[str, Any]) -> TradeThesis:
        # Synthesize agent perspectives into a cohesive thesis
        thesis = TradeThesis(symbol=symbol)

        perspectives = agent_perspectives.get("agent_perspectives", {})

        if "Volume" in perspectives:
            thesis.volume_confirmation = perspectives["Volume"].get("thesis", "")
        if "Liquidity" in perspectives:
            thesis.liquidity_context = perspectives["Liquidity"].get("thesis", "")
        if "SectorIntelligence" in perspectives:
            thesis.sector_context = perspectives["SectorIntelligence"].get("thesis", "")

        thesis.archetype = self._determine_archetype(perspectives)
        thesis.confidence_score = agent_perspectives.get("average_confidence", 0.0)

        # Define invalidation
        thesis.invalidation_criteria.append("RVOL drops below 1.0")
        thesis.invalidation_criteria.append("Liquidity vacuum detected on bid side")

        return thesis
