import asyncio
from dataclasses import replace

from src.apitConnect.event import EventType
from src.apitConnect.models.model import _Client, FetchScript
from src.apitConnect.core.endpoint import (
    ACCOUNT_ENDPOINT,
    SUMMARY_ENDPOINT,
    SUPPORTED_TICKERS_ENDPOINT,
    ADDITIONAL_INFO,
    MARKET_VALUE_ORDER_ENDPOINT,
    CLOSE_ORDER_ENDPOINT,
    SETTINGS_ENDPOINT,
    SWITCH_DEMO_LIVE_ENDPOINT,
)


class Api:
    """Full API wrapper for Trading212 using a _Client instance."""

    def __init__(self, client: _Client, mode: str = "demo"):
        self.client = client
        self._mode = mode
        self.service_url = f"https://{mode}.services.trading212.com"
        self.event_bus = getattr(client, "event_bus", None)  # optional, if client exposes it

    # Core Execute Method
    async def _execute(self, request_template: FetchScript, **updates):
        """Clone and execute a FetchScript using client.page/session headers."""
        # Inject base URL
        req = replace(request_template, base=self.service_url, **updates)
        req.validate()

        # Execute request using the _Client instance
        if not hasattr(self.client, "request"):
            raise AttributeError("Client instance must implement 'request(req)'")
        return await self.client.request(req)

    # REST V1
    async def account(self):
        data = await self._execute(ACCOUNT_ENDPOINT)
        if self.event_bus:
            await self.event_bus.emit(EventType.API_RESPONSE, {"data": data})
        return data

    async def summary(self):
        data = await self._execute(SUMMARY_ENDPOINT)
        if self.event_bus:
            await self.event_bus.emit(EventType.API_RESPONSE, {"data": data})
        return data

    async def supported_tickers(self):
        xtc = self.client.auth._x_trader
        data = await self._execute(SUPPORTED_TICKERS_ENDPOINT, x_trader_client=xtc)
        if self.event_bus:
            await self.event_bus.emit(EventType.API_RESPONSE, {"data": data})
        return data

    async def additional_info(self, **payload):
        return await self._execute(ADDITIONAL_INFO, **payload)

    # REST V2
    async def market_order(self, symbol: str, quantity: str):
        xtc = self.client.auth._x_trader
        data = await self._execute(
            MARKET_VALUE_ORDER_ENDPOINT,
            body={"ticker": symbol, "value": quantity, "targetPrice": 0},
            x_trader_client=xtc,
        )
        if self.event_bus:
            await self.event_bus.emit(EventType.API_RESPONSE, {"data": data})
        return data

    async def close_position(self, symbol: str):
        xtc = self.client.auth._x_trader
        data = await self._execute(
            CLOSE_ORDER_ENDPOINT, query={"symbol": symbol}, x_trader_client=xtc
        )
        if self.event_bus:
            await self.event_bus.emit(EventType.API_RESPONSE, {"data": data})
        return data

    # REST V3
    async def settings(self, ticker: str):
        xtc = self.client.auth._x_trader
        data = await self._execute(
            SETTINGS_ENDPOINT, body={"ticker": ticker}, x_trader_client=xtc
        )
        if self.event_bus:
            await self.event_bus.emit(EventType.API_RESPONSE, {"data": data})
        return data

    async def switch_session(self, base_url: str):
        """Switch between demo and live sessions and update _mode."""
        xtc = self.client.auth._x_trader
        aid = self.client.auth._account_id
        self.service_url = base_url  # update API URL automatically

        data = await self._execute(
            SWITCH_DEMO_LIVE_ENDPOINT,
            body={"accountId": aid},
            x_trader_client=xtc,
        )

        # Update _mode based on URL
        self._mode = "demo" if "demo" in base_url else "live"

        # Update session flags
        if "demo" in base_url:
            self.client.auth._demo_session = True
        else:
            self.client.auth._live_session = True

        return data
    
    async def ensure_dual_sessions(self):
        """Ensure both demo and live sessions exist, auto-switching if needed."""
        if not self.client.auth._demo_session:
            await self.switch_session("https://demo.services.trading212.com")
        if not self.client.auth._live_session:
            await self.switch_session("https://live.services.trading212.com")