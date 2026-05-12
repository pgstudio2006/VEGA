from dataclasses import dataclass
import logging

logger = logging.getLogger("vega.intelligence.options")

@dataclass
class OptionsMetrics:
    gamma_exposure: float = 0.0 # GEX
    gamma_flip_level: float = 0.0
    volatility_pressure: str = "COMPRESSION" # EXPANSION, COMPRESSION
    iv_percentile: float = 0.5
    dealer_positioning: str = "LONG_GAMMA" # SHORT_GAMMA
    hedging_pressure: float = 0.0

class OptionsIntelligence:
    def __init__(self):
        self.symbol_metrics = {}

    def analyze_options_flow(self, symbol: str, current_price: float, iv_data: float, gex_data: float) -> OptionsMetrics:
        dealer_pos = "LONG_GAMMA" if gex_data > 0 else "SHORT_GAMMA"

        pressure = "COMPRESSION"
        if iv_data > 0.8:
            pressure = "EXPANSION"

        metrics = OptionsMetrics(
            gamma_exposure=gex_data,
            gamma_flip_level=current_price * 0.95, # Simplified
            volatility_pressure=pressure,
            iv_percentile=iv_data,
            dealer_positioning=dealer_pos,
            hedging_pressure=abs(gex_data) * 0.1
        )
        self.symbol_metrics[symbol] = metrics
        return metrics
