import json
import logging
from typing import Any, Optional, Tuple, Dict, Callable

from src.apitConnect.event import event_bus, Event
from src.apitConnect.models.websocket import (
    TickerModel, ScheduleBatchModel, MarketScheduleItem, 
    AccountModel, PositionModel, WSModel
)

# Configure basic logging
logger = logging.getLogger(__name__)

async def enrich(data: WSModel) -> WSModel:
    """
    Optional async enrichment step. 
    Modify or wrap the data class before it hits the Event Bus.
    """
    return data

class Trading212Socket:
    def __init__(self):
        self.event_bus = event_bus
        # Map event names to specialized sanitizers
        self._dispatch_map: Dict[str, Callable] = {
            "working-schedule-sync": self._parse_schedule,
            "pos": self._parse_account,  # Ensure this matches the actual T212 event name
        }

    async def setup_websocket_hooks(self, page):
        """Attach listener for live price data from the WebSocket."""
        page.on("websocket", self._on_websocket_opened)

    async def _on_websocket_opened(self, ws):
        if "streaming/events" in ws.url:
            ws.on("framereceived", self._handle_incoming_frame)

    async def _handle_incoming_frame(self, payload: str):
        """High-level entry point for incoming WS data."""
        try:
            result = await self._run_pipeline(payload)
            if not result:
                return

            event_name, raw, processed = result
            
            event = Event.pipeline(
                message=f"WS: {event_name}",
                raw=raw,
                processed=processed 
            )
            await self.event_bus.emit(event)

        except Exception as e:
            logger.error(f"WS Frame Processing Error: {e}")
            await self.event_bus.emit(
                Event.error(message="WS Pipeline Crash", error=e)
            )

    async def _run_pipeline(self, payload: str) -> Optional[Tuple[str, Any, WSModel]]:
        """Engine.IO Parse -> Extract -> Sanitize -> Enrich."""
        # 1. Parse Engine.IO (42 sequence)
        packet = self._parse_frame(payload)
        if not packet:
            return None

        # 2. Extract Event & Payload
        event_name = packet[0]
        raw_payload = packet[1]

        # 3. Sanitize (Convert to Data Classes)
        clean = self._sanitize(event_name, raw_payload)

        # 4. Enrich
        clean = await enrich(clean)

        return event_name, raw_payload, clean

    def _sanitize(self, event_name: str, payload: Any) -> WSModel:
        """Determines the correct model based on payload type and event name."""
        
        # Priority 1: String-based Ticker Data
        if isinstance(payload, str):
            return self._parse_ticker(payload)

        # Priority 2: Named events (Schedule, Account, etc.)
        if event_name in self._dispatch_map:
            return self._dispatch_map[event_name](payload)

        # Fallback: Generic structures
        if isinstance(payload, (list, dict)):
            return {"type": "generic_data", "data": payload}

        return {"type": "unknown", "raw": payload}

    # --- Specialized Parsers ---

    def _parse_ticker(self, payload: str) -> WSModel:
        """Parses pipe-delimited price strings."""
        parts = payload.split("|")
        if len(parts) < 5:
            return {"type": "malformed_ticker", "raw": payload}
        
        try:
            return TickerModel(
                channel=parts[0],
                symbol=parts[1].replace("#", ""),
                bid=float(parts[2]),
                ask=float(parts[3]),
                timestamp=int(parts[4]),
                raw=payload
            )
        except (ValueError, IndexError):
            return {"type": "ticker_parse_error", "raw": payload}

    def _parse_schedule(self, payload: list) -> ScheduleBatchModel:
        """Parses the market working hours list."""
        items = [
            MarketScheduleItem(
                id=i.get('id'),
                status=i.get('status'),
                previousStatus=i.get('previousStatus', 'UNKNOWN'),
                nextWorking=i.get('nextWorking'),
                nextClosing=i.get('nextClosing')
            ) for i in payload if isinstance(i, dict)
        ]
        return ScheduleBatchModel(count=len(items), items=items)

    def _parse_account(self, payload: dict) -> AccountModel:
        """Parses account balance and open positions."""
        raw_positions = payload.get("positions", [])
        positions = [
            PositionModel(
                id=p.get('id'),
                symbol=p.get('symbol', '').replace("#", ""),
                quantity=float(p.get('quantity', 0)),
                averagePrice=float(p.get('averagePrice', 0)),
                currentPrice=float(p.get('currentPrice', 0)),
                ppl=float(p.get('ppl', 0))
            ) for p in raw_positions
        ]
        
        return AccountModel(
            balance=float(payload.get("balance", 0)),
            equity=float(payload.get("equity", 0)),
            positions=positions
        )

    @staticmethod
    def _parse_frame(payload: str) -> Optional[list]:
        """Engine.IO Protocol: Only process '42' (message) frames."""
        if payload.startswith("42"):
            try:
                return json.loads(payload[2:])
            except json.JSONDecodeError:
                return None
        return None