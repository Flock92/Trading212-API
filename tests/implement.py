import asyncio
from src.apitConnect.core.client import Client
from src.apitConnect.core.network.api import ApiSupervisor
from src.apitConnect.ui.console.dashboard import AsyncConsoleDashboard
from src.apitConnect.core.network.api import TradingApi  # your API wrapper

async def main():
    # 1. Start client
    client = Client()
    await client.connect()

    # 2. Start API Supervisor
    api_supervisor = ApiSupervisor(client, TradingApi())
    asyncio.create_task(api_supervisor.start())

    # 3. Start dashboard
    dashboard = AsyncConsoleDashboard()
    dashboard.start()

    # 4. Keep main alive
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        api_supervisor.is_running = False
        dashboard.stop()

if __name__ == "__main__":
    asyncio.run(main())