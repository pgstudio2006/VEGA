from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger("vega.memory.learning")

class AdaptiveLearningEngine:
    """Analyzes closed trades to refine probabilistic edge and adapt market behavior."""
    def __init__(self):
        self.performance_by_regime: Dict[str, Dict[str, float]] = {}
        self.false_positives: List[Dict[str, Any]] = []

    def review_closed_trade(self, symbol: str, entry_price: float, exit_price: float,
                            thesis: str, ecology: Any, confidence_at_entry: float):

        pnl_pct = (exit_price - entry_price) / entry_price
        is_win = pnl_pct > 0

        regime = ecology.regime
        if regime not in self.performance_by_regime:
            self.performance_by_regime[regime] = {"wins": 0, "losses": 0, "total_pnl": 0.0}

        stats = self.performance_by_regime[regime]
        if is_win:
            stats["wins"] += 1
        else:
            stats["losses"] += 1
            if confidence_at_entry > 0.85:
                 # High confidence loss -> Analyze as a potential false positive
                 self.false_positives.append({
                     "symbol": symbol,
                     "thesis": thesis,
                     "regime": regime,
                     "pnl_pct": pnl_pct
                 })
                 logger.info(f"[{symbol}] High-confidence loss recorded for false-positive analysis.")

        stats["total_pnl"] += pnl_pct

        win_rate = stats["wins"] / (stats["wins"] + stats["losses"])
        logger.info(f"Post-Trade Learning: {regime} regime win rate adjusted to {win_rate:.2%}")

    def get_regime_confidence_modifier(self, regime: str) -> float:
        """Returns a modifier to scale agent confidence based on historical regime performance."""
        stats = self.performance_by_regime.get(regime)
        if not stats or (stats["wins"] + stats["losses"]) < 5:
            return 1.0 # Not enough data

        win_rate = stats["wins"] / (stats["wins"] + stats["losses"])
        if win_rate > 0.6:
            return 1.1 # Boost confidence in favorable regimes
        elif win_rate < 0.4:
            return 0.8 # Suppress confidence in hostile regimes
        return 1.0
