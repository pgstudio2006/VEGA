from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger("vega.intelligence.filters")

class FalsePositiveFilter:
    """Aggressively filters weak setups and tracks adaptive filter effectiveness."""

    def __init__(self):
        self.rejections: Dict[str, Dict[str, Any]] = {}
        self.filter_effectiveness = {"liquidity": 0, "volatility": 0, "breadth": 0, "correlation": 0}

    def track_missed_opportunity(self, symbol: str, subsequent_performance: float):
        """Analyzes trades rejected by filters that turned out to be highly profitable (False Negatives)."""
        if symbol in self.rejections and subsequent_performance > 0.05: # > 5% move missed
            reason = self.rejections[symbol]["reason"]
            logger.warning(f"Missed Opportunity Analysis: [{symbol}] was rejected due to '{reason}' but subsequently gained {subsequent_performance:.2%}. Filter may be over-aggressive.")

    def evaluate_setup(self, symbol: str, metrics: Dict[str, Any], ecology: Any) -> Tuple[bool, str]:
        """Returns True if the setup is ACCEPTED, False if REJECTED, along with the reason."""

        # 1. Liquidity Trap Filter
        liquidity = metrics.get("liquidity_quality", 1.0)
        if liquidity < 0.2:
            reason = f"[{symbol}] REJECTED: Liquidity Trap. Quality ({liquidity:.2f}) too low for execution."
            self.filter_effectiveness["liquidity"] += 1
            self.rejections[symbol] = {"reason": "Liquidity Trap"}
            logger.debug(reason)
            return False, reason

        # 2. Volatility Instability Filter
        if ecology.volatility_regime == "EXPANDING_RAPIDLY" and metrics.get("rvol", 1.0) < 1.5:
            reason = f"[{symbol}] REJECTED: Volatility expansion without volume participation."
            self.filter_effectiveness["volatility"] += 1
            self.rejections[symbol] = {"reason": "Volatility Instability"}
            logger.debug(reason)
            return False, reason

        # 3. Market Breadth Filter
        if ecology.breadth_score < 0.3 and metrics.get("relative_strength", 1.0) < 1.1:
            reason = f"[{symbol}] REJECTED: Weak market breadth and insufficient relative strength."
            self.filter_effectiveness["breadth"] += 1
            self.rejections[symbol] = {"reason": "Weak Breadth"}
            logger.debug(reason)
            return False, reason

        # 4. Correlation Risk Filter
        if ecology.risk_on_off == "RISK_OFF" and ecology.correlation_regime == "HIGH":
            # In a highly correlated risk-off environment, long setups are inherently lower probability
            if metrics.get("direction", "LONG") == "LONG":
                reason = f"[{symbol}] REJECTED: High correlation risk-off environment hostile to long setups."
                self.filter_effectiveness["correlation"] += 1
                self.rejections[symbol] = {"reason": "Correlation Risk"}
                logger.debug(reason)
                return False, reason

        return True, "Setup passed false positive filters."
