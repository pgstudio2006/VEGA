from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
import time
from typing import Dict, Any

from vega.core.lifecycle import OpportunityState

class TerminalUI:
    def __init__(self):
        self.console = Console()

    def generate_layout(self) -> Layout:
        layout = Layout()
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=3)
        )
        layout["main"].split_row(
            Layout(name="market_structure", ratio=1),
            Layout(name="agent_reasoning", ratio=2),
            Layout(name="active_positions", ratio=1)
        )
        return layout

    def render_header(self) -> Panel:
        return Panel("[bold cyan]VEGA Autonomous Market Intelligence Operating System[/bold cyan]", style="blue")

    def render_market_structure(self, ecology: Any) -> Panel:
        content = f"Market Regime: [bold yellow]{ecology.regime}[/bold yellow]\n"
        content += f"Volatility: [magenta]{ecology.volatility_regime}[/magenta]\n"
        content += f"Liquidity: [cyan]{ecology.liquidity_regime}[/cyan]\n"
        content += f"Risk Status: [red]{ecology.risk_on_off}[/red]\n"
        content += f"Breadth Score: {ecology.breadth_score:.2f}\n"
        return Panel(content, title="Live Market Ecology")

    def render_agent_reasoning(self, intelligence_data: Dict[str, Any], leaders: list) -> Panel:
        table = Table(title=f"Live Watchtower (Leaders: {', '.join(leaders) if leaders else 'None'})")
        table.add_column("Symbol")
        table.add_column("Lifecycle State")
        table.add_column("Conviction")
        table.add_column("Action / Status")

        for symbol, data in intelligence_data.items():
            state = data.get("state", "OBSERVING")
            conf = data.get("confidence", 0.0)
            align_str = f"{conf*100:.0f}%"

            if state == "EXECUTION_READY" or state == "EXECUTING":
                action = "[bold green]EXECUTING / READY[/bold green]"
            elif state == "HIGH_CONVICTION":
                action = "[bold yellow]DEBATING / VALIDATING[/bold yellow]"
            elif state == "VALIDATING":
                 action = "[blue]VALIDATING MULTI-FACTOR[/blue]"
            else:
                action = "[dim]WATCHING / DEGRADED[/dim]"

            table.add_row(symbol, state, align_str, action)

        return Panel(table, title="Continuous Opportunity Cognition Ladder")

    def render_positions(self, positions: Dict[str, Any]) -> Panel:
        table = Table()
        table.add_column("Symbol")
        table.add_column("Size")
        table.add_column("Risk")

        for symbol, pos in positions.items():
            table.add_row(symbol, str(pos.size), f"Stop: {pos.stop_loss}")

        return Panel(table, title="Autonomous Position Management")

    def run_live(self, vega_runtime):
        layout = self.generate_layout()

        with Live(layout, refresh_per_second=2, screen=True):
            while vega_runtime.running:
                layout["header"].update(self.render_header())
                layout["market_structure"].update(self.render_market_structure(vega_runtime.market_engine.ecology))

                # Extract intelligence state from runtime
                intel_data = {}
                # Safely copy dictionary items to avoid RuntimeError: dictionary changed size during iteration
                opportunities_copy = dict(vega_runtime.lifecycle_engine.opportunities)
                for sym, opp in opportunities_copy.items():
                    if opp.state != OpportunityState.OBSERVING:
                        intel_data[sym] = {"state": opp.state.name, "confidence": opp.score}

                layout["agent_reasoning"].update(self.render_agent_reasoning(intel_data, vega_runtime.sector_leaders))

                # Safely copy active positions
                positions_copy = dict(vega_runtime.position_manager.active_positions)
                layout["active_positions"].update(self.render_positions(positions_copy))

                layout["footer"].update(Panel("VEGA Operational. Press Ctrl+C to stop.", style="dim"))
                time.sleep(0.5)
