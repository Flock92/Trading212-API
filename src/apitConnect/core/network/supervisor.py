import asyncio
from src.apitConnect.event import EventType, event_bus
from src.apitConnect.models.model import _Client
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
from src.apitConnect.core.network.api import Api  # Import the new Api class

# Map approved commands to API instance methods
APPROVED_CALLS = {
    "account": ("account", ACCOUNT_ENDPOINT),
    "summary": ("summary", SUMMARY_ENDPOINT),
    "supported_tickers": ("supported_tickers", SUPPORTED_TICKERS_ENDPOINT),
    "additional_info": ("_execute", ADDITIONAL_INFO),
    "market_order": ("market_order", MARKET_VALUE_ORDER_ENDPOINT),
    "close_position": ("close_position", CLOSE_ORDER_ENDPOINT),
    "settings": ("settings", SETTINGS_ENDPOINT),
    "switch_session": ("switch_session", SWITCH_DEMO_LIVE_ENDPOINT),
}


class ApiSupervisor:
    """Supervisor that handles API calls with dual session checks."""

    def __init__(self, client: _Client, mode: str = "demo"):
        self.client = client
        self.api = Api(client, mode=mode)  # Initialize full API class
        self.is_running = True

    async def start(self):
        """Listen for validated command requests."""
        command_queue = await event_bus.subscribe(EventType.API_REQUEST)
        print("API Supervisor: Online and listening...")

        while self.is_running:
            try:
                args, kwargs = await command_queue.get()
                command = kwargs.get("command")
                payload = kwargs.get("payload", {})

                if command not in APPROVED_CALLS:
                    await event_bus.emit(
                        EventType.API_RESPONSE,
                        {"error": f"Command '{command}' not approved"},
                    )
                    continue

                await self.dispatch(command, payload)

            except Exception as e:
                await self.client.event_bus.emit(
                    EventType.API_RESPONSE,
                    {"error": f"Supervisor Loop Error: {str(e)}"},
                )

    async def dispatch(self, command: str, payload: dict):
        """Execute API calls safely with session auto-check and injection."""
        method_name, endpoint = APPROVED_CALLS[command]
        method = getattr(self.api, method_name)

        try:
            # Ensure both demo and live sessions are present
            await self.api.ensure_dual_sessions()

            # Auto-inject x_trader_client and accountId if missing
            if "x_trader_client" not in payload:
                payload["x_trader_client"] = self.client.auth._x_trader
            if "accountId" not in payload:
                payload["accountId"] = self.client.auth._account_id

            # Execute API method
            if method_name == "_execute":
                result = await method(endpoint, **payload)
            else:
                result = await method(**payload)

            # Mask sensitive info before sending to the client/UI
            result = self._mask_sensitive(result)

            await self.client.event_bus.emit(EventType.API_RESPONSE, result)

        except Exception as e:
            await self.client.event_bus.emit(
                EventType.API_RESPONSE,
                {"error": f"Dispatch Error: {str(e)}"},
            )

    def _mask_sensitive(self, result):
        """Mask sensitive fields in API responses."""
        sensitive_keys = (
            "x_trader_client",
            "accountId",
            "trading212_session_demo",
            "trading212_session_live",
        )

        if isinstance(result, dict):
            result = result.copy()
            for key in sensitive_keys:
                if key in result:
                    result[key] = "***"
            return result

        # For _Client objects, just show a safe representation
        from src.apitConnect.models.model import _Client
        if isinstance(result, _Client):
            return repr(result)

        return result