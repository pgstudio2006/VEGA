import logging
import threading
import time
import random

from vega.core.runtime import VegaRuntime
from vega.core.lifecycle import OpportunityState
from vega.intelligence.architecture import CognitiveRouter
from vega.agents.society import AgentSociety
from vega.intelligence.market_structure import MarketStructureEngine
from vega.execution.position_manager import PositionManager
from vega.execution.thesis import ThesisEngine
from vega.infrastructure.reliability import RuntimeGuardian
from vega.ui.terminal import TerminalUI
from vega.memory.learning import PerformanceIntelligenceEngine
from vega.intelligence.openrouter_client import OpenRouterClient

logging.basicConfig(level=logging.WARNING) # Reduce noisy logs for UI

class VegaSystem(VegaRuntime):
    """The fully realized autonomous market intelligence operating system."""
    def __init__(self):
        super().__init__()
        self.openrouter_client = OpenRouterClient()
        self.router = CognitiveRouter()
        self.society = AgentSociety()
        self.market_engine = MarketStructureEngine()
        self.position_manager = PositionManager()
        self.thesis_engine = ThesisEngine()
        self.performance_engine = PerformanceIntelligenceEngine()
        self.guardian = RuntimeGuardian()
        self.ui = TerminalUI()

    def start(self):
        self.running = True
        self.guardian.ensure_recovery()

        # Start core loop in a background thread
        logic_thread = threading.Thread(target=self._loop, daemon=True)
        logic_thread.start()

        # Start UI in main thread
        try:
            self.ui.run_live(self)
        except KeyboardInterrupt:
            self.stop()

    def _observe(self):
        # Update Market Ecology
        self.market_engine.ecology.update({"regime": random.choice(["RISK_ON", "RISK_OFF", "TRANSITION", "VOLATILITY_EXPANSION"])})

        for symbol in self.watch_universe:
            score = random.random()
            # Feed into lifecycle
            self.lifecycle_engine.evaluate(symbol, score, {})

    def _analyze(self):
        super()._analyze() # Run watchtower logic

        for symbol, opp in list(self.lifecycle_engine.opportunities.items()):
            if opp.state == OpportunityState.HIGH_CONVICTION:
                # 1. Check False Positives
                is_valid, reason = self.fp_filter.evaluate_setup(symbol, opp.metrics, self.market_engine.ecology)
                if not is_valid:
                    opp.transition(OpportunityState.OBSERVING, f"False Positive Rejected: {reason}")
                    continue

                # 2. Trigger Agent Society Debate
                perspectives = self.society.gather_perspectives(symbol)

                if perspectives["is_aligned"]:
                    opp.transition(OpportunityState.EXECUTION_READY, "Society Aligned. High Conviction validated.")
                    # Move to execution
                    self._execute(symbol, perspectives)
                else:
                    opp.transition(OpportunityState.VALIDATING, "Agent debate lacked consensus.")

    def _execute(self, symbol, perspectives):
        opp = self.lifecycle_engine.opportunities[symbol]
        opp.transition(OpportunityState.EXECUTING, "Routing to execution")

        # Formulate full thesis
        thesis = self.thesis_engine.formulate_thesis(symbol, perspectives)

        price = 100.0 + random.random() * 50
        self.position_manager.open_position(
            symbol=symbol,
            price=price,
            size=10.0,
            stop_loss=price * 0.95,
            thesis=thesis,
            metrics=opp.metrics
        )
        opp.transition(OpportunityState.MONITORING, "Position opened")

    def _wait(self):
        # Monitor open positions
        current_prices = {sym: pos.entry_price * (1 + random.uniform(-0.02, 0.03)) for sym, pos in self.position_manager.active_positions.items()}
        self.position_manager.monitor_positions(
            current_prices,
            market_confidence=0.8,
            ecology_stress=self.market_engine.assess_market_stress(),
            current_ecology=self.market_engine.ecology,
            performance_engine=self.performance_engine
        )

        # Periodically close simulated positions to trigger learning logic
        if random.random() < 0.1 and self.position_manager.active_positions:
            sym_to_close = list(self.position_manager.active_positions.keys())[0]
            self.position_manager.close_position(
                sym_to_close,
                exit_price=current_prices.get(sym_to_close, 100.0),
                current_ecology=self.market_engine.ecology,
                performance_engine=self.performance_engine
            )

        time.sleep(1)

def main():
    vega = VegaSystem()
    vega.start()

if __name__ == "__main__":
    main()
