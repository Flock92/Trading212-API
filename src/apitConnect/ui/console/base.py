# src/apitConnect/ui/bootstrap.py

from src.apitConnect.ui.console import AsyncSpinner, AsyncConsoleDashboard
from src.apitConnect.event import EventType, event_bus


async def setup_ui():
    # Spinner listens to SYSTEM + ERROR
    spinner = AsyncSpinner("Working...")
    await spinner.attach(EventType.SYSTEM)  # Pass event type explicitly
    await spinner.attach(EventType.ERROR)

    # Dashboard listens to pipeline data
    # dashboard = AsyncConsoleDashboard("WebSocket Feed")
    # await dashboard.attach(EventType.PIPELINE)

    return {
        "spinner": spinner,
    }

    #"dashboard": dashboard,