from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger("vega.intelligence.filters")

class FalsePositiveFilter:
    """Aggressively filters weak setups to preserve capital and expected edge."""

    def __init__(self):
        self.rejection_reasons = []

    def evaluate_setup(self, symbol: str, metrics: Dict[str, Any], ecology: Any) -> Tuple[bool, str]:
        """Returns True if the setup is ACCEPTED, False if REJECTED, along with the reason."""

        # 1. Liquidity Trap Filter
        liquidity = metrics.get("liquidity_quality", 1.0)
        if liquidity < 0.2:
            reason = f"[{symbol}] REJECTED: Liquidity Trap. Quality ({liquidity:.2f}) too low for execution."
            logger.debug(reason)
            return False, reason

        # 2. Volatility Instability Filter
        if ecology.volatility_regime == "EXPANDING_RAPIDLY" and metrics.get("rvol", 1.0) < 1.5:
            reason = f"[{symbol}] REJECTED: Volatility expansion without volume participation."
            logger.debug(reason)
            return False, reason

        # 3. Market Breadth Filter
        if ecology.breadth_score < 0.3 and metrics.get("relative_strength", 1.0) < 1.1:
            reason = f"[{symbol}] REJECTED: Weak market breadth and insufficient relative strength."
            logger.debug(reason)
            return False, reason

        # 4. Correlation Risk Filter
        if ecology.risk_on_off == "RISK_OFF" and ecology.correlation_regime == "HIGH":
            # In a highly correlated risk-off environment, long setups are inherently lower probability
            if metrics.get("direction", "LONG") == "LONG":
                reason = f"[{symbol}] REJECTED: High correlation risk-off environment hostile to long setups."
                logger.debug(reason)
                return False, reason

        return True, "Setup passed false positive filters."
