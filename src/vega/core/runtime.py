import time
import logging
from typing import List

from vega.core.lifecycle import LifecycleEngine
from vega.intelligence.filters import FalsePositiveFilter
from vega.infrastructure.upstox_client import UpstoxLiveClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("vega.runtime")

class VegaRuntime:
    def __init__(self):
        self.running = False
        self.lifecycle_engine = LifecycleEngine()
        self.fp_filter = FalsePositiveFilter()
        self.watch_universe: List[str] = ["SPY", "QQQ", "IWM", "AAPL", "NVDA", "TSLA"]
        self.sector_leaders: List[str] = []

        # Live Data Layer
        self.upstox_client = UpstoxLiveClient()

    def start(self):
        self.upstox_client.start_background_feed()
        self.running = True
        logger.info("VEGA Runtime starting. Entering continuous observation mode.")
        try:
            self._loop()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.running = False
        logger.info("VEGA Runtime stopping gracefully.")

    def _loop(self):
        while self.running:
            self._observe()
            self._analyze()
            self._wait()

    def _observe(self):
        # Layer 1: Cheap continuous observation via live feed
        logger.debug("Observing live market conditions...")
        for symbol in self.watch_universe:

            # Fetch live quote data (fallback to simulation if keys are missing)
            live_price = self.upstox_client.fetch_live_quote(symbol)

            # In a full integration, these metrics derive directly from the WS feed
            import random
            vol_score = random.uniform(0.5, 1.5) # RVOL
            liq_score = random.uniform(0.0, 1.0) # Quality
            rs_score = random.uniform(0.8, 1.2)  # Relative Strength

            # Probabilistic scoring combining factors
            base_score = (vol_score * 0.4) + (liq_score * 0.3) + (rs_score * 0.3)
            normalized_score = min(1.0, max(0.0, (base_score - 0.5) / 1.0))

            metrics = {
                "rvol": vol_score,
                "liquidity_quality": liq_score,
                "relative_strength": rs_score,
                "volatility_structure": "COMPRESSION",
                "live_price": live_price
            }

            self.lifecycle_engine.evaluate(symbol, normalized_score, metrics)

    def _analyze(self):
        # Dynamic ranked watchlists based on continuous observation
        ranked_opps = sorted(
            [opp for opp in self.lifecycle_engine.opportunities.values() if opp.state.name != "OBSERVING"],
            key=lambda x: x.score,
            reverse=True
        )

        # Maintain live watchtower of leaders
        self.sector_leaders = [opp.symbol for opp in ranked_opps[:3]]

        for opp in ranked_opps:
            # Apply false positive filter dynamically during transitions
            if opp.state.name in ["VALIDATING", "HIGH_CONVICTION"]:
                # In the real system, ecology would be passed here
                # Simulation placeholder logic:
                # is_valid, reason = self.fp_filter.evaluate_setup(opp.symbol, opp.metrics, self.market_engine.ecology)
                pass

            if opp.state.name in ["EMERGING", "VALIDATING", "HIGH_CONVICTION"]:
                logger.info(f"[{opp.symbol}] Watchtower Update - Score: {opp.score:.2f} - State: {opp.state.name}")
                # Trigger Layer 2 or Layer 3 reasoning here based on ranking

    def _wait(self):
        # The system should spend most of its time watching and analyzing
        time.sleep(2)  # In reality, wait for next tick or interval
