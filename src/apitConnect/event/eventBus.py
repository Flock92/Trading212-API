from typing import Dict, List
import asyncio
from collections import defaultdict
from .events import EventType, Event
from dataclasses import dataclass
from typing import Awaitable, Callable

class AsyncEventBus:
    def __init__(self):
        self._queues: Dict[EventType, List[asyncio.Queue]] = defaultdict(list)

    async def subscribe(self, event_type: EventType) -> asyncio.Queue:
        queue = asyncio.Queue()
        self._queues[event_type].append(queue)
        return queue

    async def emit(self, event: Event):
        for queue in self._queues[event.type]:
            await queue.put(event)



@dataclass
class Listener:
    event_type: EventType
    handler: Callable[[Event], Awaitable[None]]
    condition: Callable[[Event], bool] = lambda e: True

    async def start(self, bus: AsyncEventBus):
        queue = await bus.subscribe(self.event_type)

        while True:
            event = await queue.get()

            if not self.condition(event):
                continue

            try:
                await self.handler(event)
            except Exception as e:
                print(f"[Listener Error]: {e}")