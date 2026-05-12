from typing import Dict, List, Any
from vega.agents.base import (
    BaseAgent, SectorIntelligenceAgent, VolumeAgent,
    LiquidityAgent, OptionsGammaAgent, BreadthAgent, RiskAgent
)
import logging

logger = logging.getLogger("vega.agents.society")

class AgentSociety:
    """Coordinates specialized agents to form a probabilistic market understanding through debate and scoring."""

    def __init__(self):
        self.agents: List[BaseAgent] = [
            SectorIntelligenceAgent(),
            VolumeAgent(),
            LiquidityAgent(),
            OptionsGammaAgent(),
            BreadthAgent(),
            RiskAgent()
        ]

    def gather_perspectives(self, symbol: str) -> Dict[str, Any]:
        perspectives = {}
        total_confidence = 0.0

        for agent in self.agents:
            evaluation = agent.evaluate(symbol)
            perspectives[agent.name] = evaluation
            total_confidence += evaluation.get("confidence", 0.0)

        avg_confidence = total_confidence / len(self.agents) if self.agents else 0.0

        # Determine alignment
        aligned = avg_confidence >= 0.8
        if aligned:
            logger.info(f"[{symbol}] Agent Society Alignment Achieved (Confidence: {avg_confidence:.2f})")

        return {
            "symbol": symbol,
            "average_confidence": avg_confidence,
            "is_aligned": aligned,
            "agent_perspectives": perspectives
        }
