import argparse
import asyncio
from contextlib import suppress

from dotenv import load_dotenv

from src.apitConnect.core.client import PlaywrightConnect
from src.apitConnect.core.browser.shutdown import graceful_shutdown
from src.apitConnect.core.network.supervisor import ApiSupervisor

from src.apitConnect.ui.console import setup_ui, AsyncConsoleDashboard

from src.gui import run_gui
from src.tui.terminal import run_tui
from src.web.server import run_web_server



async def run_console(headless: bool, username: str, password: str):
    # 1. Setup UI
    ui = await setup_ui()
    dashboard: AsyncConsoleDashboard = ui.get("dashboard")

    async with PlaywrightConnect(headless).with_credentials(username, password) as client:
        # 2. Start Supervisor
        supervisor = ApiSupervisor(client)
        supervisor_task = asyncio.create_task(supervisor.start())

        # 3. Attach dashboard to events
        await dashboard.attach()  # defaults to SYSTEM if none passed

        print("System is running. Press Ctrl+C to exit.")

        try:
            while True:
                await asyncio.sleep(1)

        except asyncio.CancelledError:
            pass

        finally:
            # Shutdown sequence
            supervisor.is_running = False
            supervisor_task.cancel()

            with suppress(asyncio.CancelledError):
                await supervisor_task

            dashboard.stop()

            with suppress(Exception):
                await graceful_shutdown(client)


def main():
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Apit212: Professional Trading 212 SDK & Interface"
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument("--gui", action="store_true", help="Launch Desktop GUI")
    group.add_argument("--tui", action="store_true", help="Launch Terminal UI")
    group.add_argument("--web", action="store_true", help="Start API Server")

    parser.add_argument(
        "--headless",
        action="store_true",
        default=True,
        help="Run browser in headless mode (default: True)",
    )

    parser.add_argument("--username", type=str, help="Login username")
    parser.add_argument("--password", type=str, help="Login password")

    args = parser.parse_args()

    # Fallback to env vars if not provided
    username = args.username or "YOUR_USERNAME"
    password = args.password or "YOUR_PASSWORD"

    try:
        if args.gui:
            # GUI owns loop
            run_gui(client=PlaywrightConnect(False))

        elif args.web:
            asyncio.run(run_web_server(headless=args.headless))

        else:
            # Default → TUI/console mode
            asyncio.run(run_console(args.headless, username, password))

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")


if __name__ == "__main__":
    main()