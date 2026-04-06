# **Apit212** 🚀

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Apit212** I stopped updating the original Apit212 when Trading212 launched their own API, but since they never added CFD support, I'm back to finish what I started. This new version will include a GUI and a TUI for trading and portfolio monitoring. I'm aiming to have all the big changes done by the end of the week!

> [!WARNING]  
> **Disclaimer:** This project is not affiliated with, maintained, or endorsed by Trading 212. Use this API at your own risk. The developers are not responsible for any financial losses or account actions resulting from the use of this software.

## ✨ Features
* **CFD Support:** Execute trades where the official API cannot.
* **Playwright Powered:** Robust browser automation that handles modern web updates.
* **Multiple Interfaces:** Modular support for CLI, TUI, and GUI interactions.
* **Data Scraping:** Easily extract real-time market data for analysis.

---

## 🛠 Installation

Install the package via pip:

```bash
pip install apit212

🚀 Quick Start: Running the Dashboard

To launch the full suite—including the WebSocket client, the API Supervisor for trade execution, and the interactive Console Dashboard—you can use the following implementation.

This setup initializes the core Client, starts the ApiSupervisor in a background task to handle incoming trade requests, and boots the AsyncConsoleDashboard.
Python

import asyncio
from src.apitConnect.core.client import Client
from src.apitConnect.core.network.supervisor import ApiSupervisor
from src.apitConnect.ui.console.dashboard import AsyncConsoleDashboard

async def main():
    # 1. Initialize and connect the WebSocket client
    client = Client()
    await client.connect()

    # 2. Start the API Supervisor (Handles CFD Orders & Account Actions)
    # The supervisor runs as a background task listening to the internal EventBus
    api_supervisor = ApiSupervisor(client, mode="demo")
    asyncio.create_task(api_supervisor.start())

    # 3. Start the Interactive Dashboard (GUI/TUI)
    dashboard = AsyncConsoleDashboard()
    dashboard.start()

    # 4. Keep the event loop alive
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        api_supervisor.is_running = False
        dashboard.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
