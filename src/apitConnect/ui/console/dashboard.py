from datetime import datetime
from typing import Any

from rich.console import Console
from rich.json import JSON
from rich.panel import Panel
from rich.rule import Rule


class AsyncConsoleDashboard:
    def __init__(self, title: str = "System Monitor"):
        self._console = Console()
        self._title = title

    async def attach(self, signal: Any, event_name: str):
        """Subscribes to a signal and directs updates to the printer."""
        await signal.on(
            event_name=event_name,
            callback=self.handle_update,
        )

    async def handle_update(self, update: Any):
        data = getattr(update, "data", update)
        description = getattr(update, "description", "Response Received")
        timestamp = datetime.now().strftime("%H:%M:%S")

        self._console.print()
        self._console.print(
            Rule(title=f"[bold cyan]{self._title}[/bold cyan]", style="blue")
        )

        self._console.print(
            f"[bold dim]{timestamp}[/bold dim] | [green]EVENT:[/green] {description}"
        )

        if data:
            json_renderable = JSON.from_data(data, indent=4)
            self._console.print(
                Panel(json_renderable, border_style="dim", expand=False, padding=(1, 2))
            )
        else:
            self._console.print("[yellow]No data payload received.[/yellow]")

        self._console.print(Rule(style="dim"))

    def start(self):
        pass

    def stop(self):
        pass