from getpass import getpass
from typing import Dict, Optional

from src.apitConnect.auth import StoredAuth
from src.apitConnect.connector import PlaywrightConnector
from src.apitConnect.endpoints import API
from src.apitConnect.fetch.account import fetch_account
from src.apitConnect.fetch.summary import fetch_summary
from src.apitConnect.fetch.supported_tickers import fetch_supported_tickers
from src.apitConnect.fetch.value import value as fetch_value_order
from src.apitConnect.session import AsyncSessionManager


class Client:
    def __init__(
        self, base_url: str = "https://app.trading212.com/", headless: bool = True
    ):
        self.base_url = base_url
        self.headers: Optional[Dict[str, str]] = None
        self._session: Optional[AsyncSessionManager] = None
        self._api: Optional[API] = None
        self.connector = PlaywrightConnector(self.base_url, headless=headless)
        self.mode = "demo"

    async def connect(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        login_path: str = "/",
    ) -> API:
        """Initializes Playwright, authenticates, and sets up session managers."""
        if not username:
            username = input("Username: ")
        if not password:
            password = getpass("Password: ")

        # Perform authentication via Playwright
        auth: StoredAuth = await self.connector.authenticate(
            username=username, password=password, login_path=login_path
        )

        # Initialize the session manager
        self._session = AsyncSessionManager(
            self.base_url,
            access_token=auth.access_token,
            refresh_token=auth.refresh_token,
            refresh_endpoint="/auth/refresh",
        )

        # Sync browser cookies to the session manager
        if auth.cookies:
            self._session.sync_playwright_cookies(auth.cookies)

        self._api = API(self._session)
        self.headers = auth.headers

        print(f"Successfully connected to {self.base_url}")
        return self._api

    def _get_trader_client(self) -> str:
        """Internal helper to retrieve the x-trader-client header."""
        if not self.headers:
            raise RuntimeError("Client not connected. Call connect() first.")
        return self.headers.get("x-trader-client", "")

    async def stay_active(self):
        """Simulate human presence to prevent idle timeouts."""
        if self.connector.page:
            await self.connector.page.mouse.move(100, 100)
            await self.connector.page.mouse.move(200, 200)

    def api(self) -> API:
        """Returns the API instance if connected."""
        if not self._api:
            raise RuntimeError("Not connected: call connect() first")
        return self._api

    async def fetch_supported_tickers(self):
        """Fetches the supported tickers"""
        return await fetch_supported_tickers(self, self._get_trader_client())

    async def fetch_summary(self):
        """Fetches the account summary."""
        return await fetch_summary(self, self._get_trader_client())

    async def fetch_account(self):
        """Fetches account-specific details."""
        return await fetch_account(self, self._get_trader_client())

    async def execute_value_order(
        self,
        ticker: str,
        value: float,
        target_price: float,
        stoploss: float = 0.0,
        takeprofit: float = 0.0,
    ):
        """Executes a value-based order by forwarding all parameters."""

        # We get the trader client automatically from our internal helper
        x_trader_client = self._get_trader_client()

        # Forward everything to the actual fetch logic
        return await fetch_value_order(
            self, x_trader_client, ticker, value, target_price, stoploss, takeprofit
        )

    async def close(self):
        """Gracefully shuts down the session and the Playwright browser."""
        print("Closing session and browser...")
        if self._session:
            await self._session.close()
        await self.connector.shutdown()
