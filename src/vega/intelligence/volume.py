from dataclasses import dataclass
import logging

logger = logging.getLogger("vega.intelligence.volume")

@dataclass
class VolumeMetrics:
    rvol: float = 1.0  # Relative Volume
    volume_delta: float = 0.0
    accumulation_distribution: str = "NEUTRAL"
    participation_intensity: float = 0.5
    exhaustion_detected: bool = False

class VolumeIntelligence:
    def __init__(self):
        self.symbol_metrics = {}

    def analyze_volume(self, symbol: str, current_vol: float, avg_vol: float, price_action: float) -> VolumeMetrics:
        rvol = current_vol / avg_vol if avg_vol > 0 else 1.0

        acc_dist = "NEUTRAL"
        if rvol > 1.5:
            if price_action > 0.01:
                acc_dist = "ACCUMULATION"
            elif price_action < -0.01:
                acc_dist = "DISTRIBUTION"

        exhaustion = False
        if rvol > 3.0 and abs(price_action) < 0.005:
            exhaustion = True

        metrics = VolumeMetrics(
            rvol=rvol,
            volume_delta=current_vol - avg_vol,
            accumulation_distribution=acc_dist,
            participation_intensity=min(1.0, rvol / 2.0),
            exhaustion_detected=exhaustion
        )
        self.symbol_metrics[symbol] = metrics
        return metrics
