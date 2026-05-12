from typing import Dict, Any, List
from datetime import datetime
import json
import logging

logger = logging.getLogger("vega.memory.episodic")

class EpisodicMemory:
    """Persistent memory of market setups, outcomes, and agent reasoning."""
    def __init__(self, storage_path: str = "vega_memory.json"):
        self.storage_path = storage_path
        self.episodes: List[Dict[str, Any]] = []

    def record_episode(self, symbol: str, regime: str, setup_data: Dict[str, Any], outcome: str, pnl: float):
        episode = {
            "timestamp": datetime.utcnow().isoformat(),
            "symbol": symbol,
            "regime": regime,
            "setup": setup_data,
            "outcome": outcome,
            "pnl": pnl
        }
        self.episodes.append(episode)
        logger.info(f"Recorded Memory Episode: {symbol} in {regime} resulting in {outcome} ({pnl})")
        self._persist()

    def recall_similar(self, current_regime: str, current_setup: Dict[str, Any]) -> List[Dict[str, Any]]:
        # Simplified similarity search
        return [e for e in self.episodes if e["regime"] == current_regime]

    def _persist(self):
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.episodes, f)
        except Exception as e:
            logger.error(f"Failed to persist memory: {e}")
