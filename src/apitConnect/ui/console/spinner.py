import asyncio
from typing import Optional
from datetime import datetime

from rich.progress import Progress, SpinnerColumn, TextColumn

from src.apitConnect.event import event_bus, EventType, Event


class AsyncSpinner:
    """Rich spinner that listens to event_bus and updates dynamically."""

    def __init__(self, description: str = "Working..."):
        self._progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
        )
        self._task_id: Optional[int] = None
        self._started = False
        self._default_description = description

        self._listener_tasks = []
        self._is_running = False

    # -----------------------------
    # Lifecycle
    # -----------------------------
    def start(self):
        if not self._started:
            self._progress.start()
            self._task_id = self._progress.add_task(
                self._default_description, total=None
            )
            self._started = True

    def stop(self):
        self._is_running = False

        for task in self._listener_tasks:
            task.cancel()

        if self._started:
            self._progress.stop()
            self._started = False

    # -----------------------------
    # Attach to EventBus
    # -----------------------------
    async def attach(self, *event_types: EventType):
        """
        Attach spinner to event bus events.
        Example: await spinner.attach(EventType.SYSTEM, EventType.ERROR)
        """
        if not event_types:
            event_types = (EventType.SYSTEM, EventType.ERROR)

        self._is_running = True

        for event_type in event_types:
            queue = await event_bus.subscribe(event_type)
            task = asyncio.create_task(self._listen(queue))
            self._listener_tasks.append(task)

    async def _listen(self, queue: asyncio.Queue):
        while self._is_running:
            try:
                event: Event = await queue.get()
                await self.handle_update(event)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[Spinner Error] {e}")

    # -----------------------------
    # Event Handler
    # -----------------------------
    async def handle_update(self, event: Event):
        if not self._started:
            self.start()

        description = self._format(event)

        self._progress.update(
            self._task_id,
            description=description,
        )

    # -----------------------------
    # Formatting
    # -----------------------------
    def _format(self, event: Event) -> str:
        timestamp = datetime.now().strftime("%H:%M:%S")

        description = getattr(event, "description", "Processing...")
        status = getattr(event, "status", None)
        message = getattr(event, "data", None)

        base = f"[cyan]{description}[/cyan]"

        if status == "success":
            base = f"[green]{description}[/green]"
        elif status == "error":
            base = f"[red]{description}[/red]"

        if message:
            return f"{base} → {message} [dim]({timestamp})[/dim]"

        return f"{base} [dim]({timestamp})[/dim]"