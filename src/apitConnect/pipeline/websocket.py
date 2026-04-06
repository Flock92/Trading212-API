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
            "eqs": self._parse_ticker
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

    from typing import Optional

    def _parse_ticker(self, payload: str) -> Optional[TickerModel]:
        """Parses pipe-delimited price strings: QR|#SYMBOL|BID|ASK|TIMESTAMP"""

        # Quick guard for empty or non-string payloads
        if not payload or not isinstance(payload, str):
            return None

        parts = payload.split("|")

        # T212 QR packets usually have 5 parts
        if len(parts) < 5:
            return None

        try:
            # We strip/replace here to ensure the symbol is clean for your GUI lookups
            clean_symbol = parts[1].replace("#", "").strip()

            return TickerModel(
                channel=parts[0],
                symbol=clean_symbol,
                bid=float(parts[2]),
                ask=float(parts[3]),
                timestamp=int(parts[4]),
                raw=payload
            )
        except (ValueError, IndexError, TypeError) as e:
            # Logging the error but returning None to protect the UI
            print(f"[Ticker Parser Error] {e} for payload: {payload}")
            return None

    def _parse_schedule(self, payload: list) -> Optional[ScheduleBatchModel]:
        """Parses the market working hours list and creates a lookup table."""
        
        if not isinstance(payload, list):
            return None
    
        parsed_items = []
        lookup_table = {}
    
        for item in payload:
            if not isinstance(item, dict):
                continue
                
            m_id = item.get('id')
            if m_id is None:
                continue
            
            schedule_item = MarketScheduleItem(
                id=int(m_id),
                status=item.get('status', 'CLOSED'),
                previousStatus=item.get('previousStatus', 'UNKNOWN'),
                nextWorking=item.get('nextWorking', ''),
                nextClosing=item.get('nextClosing', '')
            )
            
            parsed_items.append(schedule_item)
            lookup_table[m_id] = schedule_item
    
        return ScheduleBatchModel(
            count=len(parsed_items), 
            items=parsed_items,
            lookup=lookup_table
        )

    def _parse_account(self, payload: dict) -> Optional[AccountModel]:
        """Parses account balance and positions into a typed AccountModel."""

        # 1. Safely navigate the nested dict
        data = payload.get("data", {})
        request = payload.get("request", [])
        cash = data.get("cash")

        # If 'cash' is missing, it's a partial update; ignore to prevent UI flickering
        if not cash or not isinstance(cash, dict):
            return None

        open_section = data.get("open", {})
        pending_section = data.get("limitStop", {})

        # 2. Extract Trade Counts
        open_count = open_section.get("unfilteredCount", 0)
        pending_count = pending_section.get("unfilteredCount", 0)

        # 3. Parse Items into PositionModel List
        raw_items = open_section.get("items", [])
        parsed_positions = []

        try:
            for item in raw_items:
                # Map raw JSON to our new PositionModel
                pos = PositionModel(
                    id=str(item.get("positionId", "")),
                    symbol=str(item.get("code", "Unknown")),
                    quantity=float(item.get("quantity", 0.0)),
                    averagePrice=float(item.get("averagePrice", 0.0)),
                    value=float(item.get("value", 0.0)),
                    margin=float(item.get("margin", 0.0)),
                    ppl=float(item.get("ppl", 0.0)),
                    fxFee=float(item.get("fxFee", 0.0)),
                    interest=float(item.get("interest", 0.0)),
                    created=str(item.get("created", ""))
                )
                parsed_positions.append(pos)

            # 4. Return the fully typed AccountModel
            return AccountModel(
                total=float(cash.get("total", 0.0)),
                free=float(cash.get("free", 0.0)),
                margin=float(cash.get("margin", 0.0)),
                ppl=float(cash.get("ppl", 0.0)),
                result=float(cash.get("result", 0.0)),
                open_trades_count=int(open_count),
                pending_orders_count=int(pending_count),
                open_items=parsed_positions  # Now a List[PositionModel]
            )

        except (ValueError, TypeError, KeyError) as e:
            print(f"[Parser Warning] Failed to parse account/position data: {e}")
            return None

    @staticmethod
    def _parse_frame(payload: str) -> Optional[list]:
        """Engine.IO Protocol: Only process '42' (message) frames."""
        if payload.startswith("42"):
            try:
                return json.loads(payload[2:])
            except json.JSONDecodeError:
                return None
        return None