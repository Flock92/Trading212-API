import asyncio
from playwright.async_api import Error as PlaywrightError
from src.apitConnect.core.browser import launch_browser, graceful_shutdown
from src.apitConnect.core.network.headers import HeaderCapture
from src.apitConnect.core.auth.login import perform_login
from src.apitConnect.models.model import ServiceURL, _Client, _Auth
from src.apitConnect.pipeline.websocket import Trading212Socket
from src.apitConnect.event import event_bus, Event


class PlaywrightConnect:
    def __init__(self, headless: bool = True):
        self.base_url = ServiceURL.BASEURL.value
        self.headless = headless
        self.header_capture = HeaderCapture()
        self.socket = Trading212Socket()
        self._client: _Client | None = None
        self._credentials = None

    async def __aenter__(self):
        if not self._credentials:
            raise ValueError("Credentials not set. Use .with_credentials()")
        username, password = self._credentials
        return await self.authenticate(username, password)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def authenticate(self, username: str, password: str) -> _Client:
        """Authenticate and return a fully populated _Client with _Auth."""
        await event_bus.emit(Event.system("Authenticating..."))

        # Launch browser and page
        playwright, browser, page = await launch_browser(self.headless)
        page.on("request", self.header_capture.handle_request)

        # Attach websocket hooks
        await self.socket.setup_websocket_hooks(page)

        # Perform login
        await perform_login(self.base_url, page, username, password)

        # Wait briefly to ensure headers are captured
        timeout = 30
        start_time = asyncio.get_event_loop().time()
        while "x-trader-client" not in self.header_capture.headers:
            if asyncio.get_event_loop().time() - start_time > timeout:
                break
            await asyncio.sleep(0.5)

        headers = self.header_capture.headers

        # Extract key session values
        x_trader = headers.get("x-trader-client", "")
        demo_session = any(c["name"] == "TRADING212_SESSION_DEMO" for c in await page.context.cookies())
        live_session = any(c["name"] == "TRADING212_SESSION_LIVE" for c in await page.context.cookies())

        # Extract account_id from x_trader header if present
        account_id = 0
        if x_trader and "accountId=" in x_trader:
            try:
                for part in x_trader.split(","):
                    if part.strip().startswith("accountId="):
                        account_id = int(part.split("=")[1])
            except (ValueError, IndexError):
                account_id = 0

        auth = _Auth(
            _x_trader=x_trader,
            _account_id=account_id,
            _demo_session=demo_session,
            _live_session=live_session,
        )

        # Build the client object
        self._client = _Client(
            playwright=playwright,
            browser=browser,
            page=page,
            headers=headers,
            auth=auth,
        )

        await event_bus.emit(Event.system("Authenticated successfully"))

        return self._client

    async def close(self):
        """Safe cleanup of the browser and page."""
        if self._client:
            try:
                await graceful_shutdown(self._client)
            except PlaywrightError as e:
                # Ignore errors caused by already-closed pages/browser
                if "Target page, context or browser has been closed" not in str(e):
                    print(f"[Playwright Warning]: {e}")
            finally:
                self._client = None

    def with_credentials(self, username: str, password: str):
        self._credentials = (username, password)
        return self