from dataclasses import dataclass
import logging

logger = logging.getLogger("vega.intelligence.liquidity")

@dataclass
class LiquidityMetrics:
    imbalance: float = 0.0 # Positive = Bid heavy, Negative = Ask heavy
    spread_width: float = 0.01
    vacuum_detected: bool = False
    sweep_detected: bool = False
    absorption_level: float = 0.0 # High means passive liquidity is absorbing aggressive flow

class LiquidityIntelligence:
    def __init__(self):
        self.symbol_metrics = {}

    def analyze_liquidity(self, symbol: str, bid_vol: float, ask_vol: float, recent_trades: list) -> LiquidityMetrics:
        total_vol = bid_vol + ask_vol
        imbalance = (bid_vol - ask_vol) / total_vol if total_vol > 0 else 0.0

        vacuum = False
        if total_vol < 100: # Arbitrary threshold for example
            vacuum = True

        metrics = LiquidityMetrics(
            imbalance=imbalance,
            spread_width=0.05 if vacuum else 0.01,
            vacuum_detected=vacuum,
            sweep_detected=len(recent_trades) > 10, # Simplified
            absorption_level=abs(imbalance) * 0.5
        )
        self.symbol_metrics[symbol] = metrics
        return metrics
