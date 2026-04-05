import asyncio
from typing import Optional
from src.apitConnect.event import event_bus, Event, EventType, Listener

class ApiService:
    def __init__(self):
        self.client = None
        self.supervisor = None
        self._bus = event_bus # Use the shared instance
        self.is_running = False
        self._listeners: list[asyncio.Task] = []

    async def start(self, username: str, password: str):
        from src.apitConnect.core.client import PlaywrightConnect
        from src.apitConnect.core.network.supervisor import ApiSupervisor

        # 1. Initialize Client
        self.client = await PlaywrightConnect(True)\
            .with_credentials(username, password)\
            .__aenter__()

        # 2. Initialize Supervisor
        self.supervisor = ApiSupervisor(self.client)
        self.is_running = True

        # 3. Start Background Tasks
        asyncio.create_task(self.supervisor.start())
        
        # Emit a system event that the service is live
        await self._bus.emit(Event.system("API Service Started and Connected"))

    async def stop(self):
        self.is_running = False

        # Cancel any active listeners managed by the service
        for task in self._listeners:
            task.cancel()

        if self.supervisor:
            self.supervisor.is_running = False

        if self.client:
            await self.client.__aexit__(None, None, None)
            
        await self._bus.emit(Event.system("API Service Stopped"))

    # --- Event Bus Integration Features ---

    async def subscribe(self, event_type: EventType) -> asyncio.Queue:
        """
        Allows external code to get a queue for a specific event type.
        Usage: queue = await api_service.subscribe(EventType.PRICE_UPDATE)
        """
        return await self._bus.subscribe(event_type)

    def add_listener(self, listener: Listener):
        """
        Registers a Listener object and runs it in the background.
        """
        task = asyncio.create_task(listener.start(self._bus))
        self._listeners.append(task)
        return task

    async def emit_custom_event(self, event: Event):
        """
        Manually push an event into the bus through the service.
        """
        await self._bus.emit(event)