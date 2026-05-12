from typing import Dict, Any, List
from datetime import datetime
import logging

logger = logging.getLogger("vega.memory.learning")

class PerformanceIntelligenceEngine:
    """Evaluates and refines probabilistic edge, tracking confidence calibration and regime performance."""
    def __init__(self):
        self.performance_by_regime: Dict[str, Dict[str, float]] = {}
        self.performance_by_archetype: Dict[str, Dict[str, float]] = {}
        self.confidence_calibration: Dict[str, Dict[str, float]] = {"high": {"wins":0, "losses":0}, "medium": {"wins":0, "losses":0}}
        self.false_positives: List[Dict[str, Any]] = []

    def _calibrate_confidence(self, confidence: float, is_win: bool):
        bucket = "high" if confidence > 0.8 else "medium"
        if is_win:
            self.confidence_calibration[bucket]["wins"] += 1
        else:
            self.confidence_calibration[bucket]["losses"] += 1

    def _track_archetype(self, archetype: str, is_win: bool, pnl_pct: float):
        if not archetype:
            return
        if archetype not in self.performance_by_archetype:
            self.performance_by_archetype[archetype] = {"wins": 0, "losses": 0, "total_pnl": 0.0}
        stats = self.performance_by_archetype[archetype]
        if is_win:
            stats["wins"] += 1
        else:
            stats["losses"] += 1
        stats["total_pnl"] += pnl_pct

    def review_closed_trade(self, symbol: str, entry_price: float, exit_price: float,
                            thesis: Any, ecology: Any, confidence_at_entry: float, execution_quality: float = 1.0):

        pnl_pct = (exit_price - entry_price) / entry_price
        is_win = pnl_pct > 0

        # 1. Calibrate Confidence
        self._calibrate_confidence(confidence_at_entry, is_win)

        # 2. Track Archetype Performance
        archetype = getattr(thesis, 'archetype', 'UNKNOWN')
        self._track_archetype(archetype, is_win, pnl_pct)

        # 3. Track Regime Performance
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
                     "archetype": archetype,
                     "regime": regime,
                     "pnl_pct": pnl_pct
                 })
                 logger.info(f"[{symbol}] High-confidence loss recorded. Confidence calibration requires adjustment.")

        stats["total_pnl"] += pnl_pct

        win_rate = stats["wins"] / (stats["wins"] + stats["losses"])

        # 4. Institutional Post-Trade Review & Alpha Attribution
        logger.info(f"Post-Trade Review [{symbol}]: Regime '{regime}' Win Rate: {win_rate:.2%}. Archetype '{archetype}' PnL: {pnl_pct:.2%}. Exec Quality: {execution_quality:.2f}")

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
