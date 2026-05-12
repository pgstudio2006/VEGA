from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger("vega.execution.position_manager")

@dataclass
class Position:
    symbol: str
    entry_price: float
    size: float
    stop_loss: float
    take_profit: Optional[float] = None
    confidence: float = 1.0
    thesis: str = ""
    opened_at: datetime = field(default_factory=datetime.utcnow)
    realized_pnl: float = 0.0

    def adapt_stop(self, new_stop: float, reason: str):
        if new_stop > self.stop_loss: # Assuming long position
            logger.info(f"[{self.symbol}] Trailing stop advanced to {new_stop:.2f} ({reason})")
            self.stop_loss = new_stop

    def partial_exit(self, exit_price: float, size_to_close: float, reason: str):
        if size_to_close >= self.size:
            return
        pnl = (exit_price - self.entry_price) * size_to_close
        self.realized_pnl += pnl
        self.size -= size_to_close
        logger.info(f"[{self.symbol}] Partial exit of {size_to_close} at {exit_price:.2f}. Reason: {reason}. Realized PnL: {pnl:.2f}")

import time

class PositionManager:
    """Manages live positions as living adaptive entities."""
    def __init__(self):
        self.active_positions: Dict[str, Position] = {}
        self.last_trade_time = 0
        self.max_daily_trades = 5
        self.trades_today = 0

    def can_trade(self) -> bool:
        """Patience & Discipline Intelligence: prevents overtrading."""
        if self.trades_today >= self.max_daily_trades:
            logger.warning("Daily trade limit reached. Forcing patience.")
            return False

        if time.time() - self.last_trade_time < 300: # 5 min cooldown
            logger.warning("Trade cooldown active. Preserving cognitive and execution bandwidth.")
            return False

        return True

    def open_position(self, symbol: str, price: float, size: float, stop_loss: float, thesis: str, metrics: Dict[str, Any] = None):
        if not self.can_trade():
            return False

        # Liquidity-sensitive sizing
        actual_size = size
        if metrics and metrics.get("liquidity_quality", 1.0) < 0.5:
            actual_size = size * 0.5
            logger.info(f"[{symbol}] Liquidity quality is low. Scaling down position size by 50%.")

        pos = Position(symbol=symbol, entry_price=price, size=actual_size, stop_loss=stop_loss, thesis=thesis)
        self.active_positions[symbol] = pos
        self.last_trade_time = time.time()
        self.trades_today += 1
        logger.info(f"Opened Position: {symbol} at {price:.2f} (Size: {actual_size:.2f}). Risk strictly defined.")
        return True

    def monitor_positions(self, current_prices: Dict[str, float], market_confidence: float, ecology_stress: float = 0.0):
        symbols_to_close = []
        for symbol, pos in self.active_positions.items():
            current_price = current_prices.get(symbol)
            if not current_price:
                continue

            # Dynamic adaptation logic
            pos.confidence = market_confidence

            # Stop loss hit
            if current_price <= pos.stop_loss:
                logger.warning(f"[{symbol}] Stop loss triggered at {current_price:.2f}. Exiting.")
                symbols_to_close.append(symbol)

            # Market Stress Liquidity Exit
            elif ecology_stress > 0.7:
                logger.warning(f"[{symbol}] Market stress critical. Force liquidating position to protect capital.")
                symbols_to_close.append(symbol)

            # Volatility/Gamma aware trailing stop & partials
            elif current_price > pos.entry_price * 1.05:
                pos.adapt_stop(current_price * 0.98, "Volatility trailing logic")
                if pos.size > 5.0 and current_price > pos.entry_price * 1.10:
                    pos.partial_exit(current_price, pos.size * 0.5, "Securing profits on volatility expansion")

            # Thesis decay exit
            elif pos.confidence < 0.4:
                 logger.info(f"[{symbol}] Thesis invalidation/confidence decay. Exiting early.")
                 symbols_to_close.append(symbol)

        for s in symbols_to_close:
            self.close_position(s)

    def close_position(self, symbol: str):
        if symbol in self.active_positions:
            del self.active_positions[symbol]
            logger.info(f"Closed Position: {symbol}")
