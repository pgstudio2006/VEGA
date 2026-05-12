from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any

class OpportunityState(Enum):
    OBSERVING = auto()
    EMERGING = auto()
    VALIDATING = auto()
    HIGH_CONVICTION = auto()
    EXECUTION_READY = auto()
    EXECUTING = auto()
    MANAGING = auto()
    EXITING = auto()
    CLOSED = auto()
    REVIEWED = auto()

@dataclass
class Opportunity:
    symbol: str
    state: OpportunityState = OpportunityState.OBSERVING
    score: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    history: list = field(default_factory=list)

    def transition(self, new_state: OpportunityState, reason: str):
        self.history.append({
            "from": self.state,
            "to": new_state,
            "reason": reason,
            "timestamp": datetime.utcnow()
        })
        self.state = new_state
        self.updated_at = datetime.utcnow()

class LifecycleEngine:
    def __init__(self):
        self.opportunities: Dict[str, Opportunity] = {}

    def track(self, symbol: str) -> Opportunity:
        if symbol not in self.opportunities:
            self.opportunities[symbol] = Opportunity(symbol=symbol)
        return self.opportunities[symbol]

    def evaluate(self, symbol: str, score: float, metrics: Dict[str, Any]):
        opp = self.track(symbol)
        opp.score = score
        opp.metrics.update(metrics)

        # Aggressive downgrading logic
        if opp.state.value > OpportunityState.OBSERVING.value and opp.state.value < OpportunityState.EXECUTING.value:
            if score < 0.4 or metrics.get("liquidity_quality", 1.0) < 0.3:
                opp.transition(OpportunityState.OBSERVING, "Setup degraded: liquidity weakened or score collapsed.")
                return

        # Progressive state machine logic based on score
        if opp.state == OpportunityState.OBSERVING and score > 0.6:
            opp.transition(OpportunityState.EMERGING, "Score exceeded emergence threshold")
        elif opp.state == OpportunityState.EMERGING and score > 0.75:
            opp.transition(OpportunityState.VALIDATING, "Emerging setup validating against market structure")
        elif opp.state == OpportunityState.VALIDATING and score > 0.85:
            opp.transition(OpportunityState.HIGH_CONVICTION, "Validation successful. High conviction achieved.")
        elif opp.state == OpportunityState.HIGH_CONVICTION and score > 0.9:
            opp.transition(OpportunityState.EXECUTION_READY, "Multi-factor alignment confirmed. Ready for execution.")
