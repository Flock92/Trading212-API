import asyncio
from src.apitConnect.event import EventType, event_bus, Event
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
import uuid

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
        self.api = Api(client, mode=mode)
        self.is_running = True

    async def start(self):
        """Listen for validated command requests."""
        command_queue = await event_bus.subscribe(EventType.API_REQUEST)
        print("API Supervisor: Online and listening...")

        while self.is_running:
            try:
                # 1. Receive the Event object
                event: Event = await command_queue.get()
                
                # 2. Extract metadata from the Event dataclass
                corr_id = event.correlation_id
                command = event.command
                payload = event.data.get("payload", {})

                if command not in APPROVED_CALLS:
                    # Send response back with the SAME correlation_id
                    await event_bus.emit(
                        Event.api_response(
                            message="error", 
                            correlation_id=corr_id, 
                            data={"error": f"Command '{command}' not approved"}
                        )
                    )
                    continue

                print("sending to dispatch")

                # 3. Pass the corr_id to dispatch
                await self.dispatch(command, payload, corr_id)

            except Exception as e:
                # Fallback for loop errors (requires a generated or nil UUID if event failed to parse)
                await event_bus.emit(
                    Event.api_response(
                        message="error", 
                        correlation_id=getattr(event, 'correlation_id', None), 
                        data={"error": f"Supervisor Loop Error: {str(e)}"}
                    )
                )

    async def dispatch(self, command: str, payload: dict, corr_id: uuid.UUID):
        """Execute API calls safely and return response with correlation_id."""
        method_name, endpoint = APPROVED_CALLS[command]
        method = getattr(self.api, method_name)

        ticker = payload.get("ticker", "TSLA")
        value = payload.get("value", 1)
        price = payload.get("targetPrice")

        print("dispatch recieved")
        print("running a mock order")
        result = await self.api.market_order(ticker, value, price)
        print(result)
        print("passed mock")


        try:
            await self.api.ensure_dual_sessions()

            # Auto-inject sensitive IDs
            if "x_trader_client" not in payload:
                payload["x_trader_client"] = self.client.auth._x_trader
            if "accountId" not in payload:
                payload["accountId"] = self.client.auth._account_id

            # Execute
            if method_name == "_execute":
                result = await method(endpoint, **payload)
            else:
                result = self.api.market_order(payload.get("ticker", "TSLA", payload.get("value", 1)))
                # result = await method(**payload)
                print(result)

            result = self._mask_sensitive(result)

            # 4. Emit response using the correlation_id from the original request
            await event_bus.emit(
                Event.api_response(
                    message="success", 
                    correlation_id=corr_id, 
                    data=result
                )
            )

        except Exception as e:
            print(e)
            await event_bus.emit(
                Event.api_response(
                    message="error", 
                    correlation_id=corr_id, 
                    data={"error": f"Dispatch Error: {str(e)}"}
                )
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