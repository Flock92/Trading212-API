from dataclasses import dataclass, field, asdict
from typing import List, Optional, Union, Dict, Any
from datetime import datetime

@dataclass(frozen=True)
class TickerModel:
    channel: str
    symbol: str
    bid: float
    ask: float
    timestamp: int
    raw: str
    type: str = "ticker"

    @property
    def mid_price(self) -> float:
        return (self.bid + self.ask) / 2

    @property
    def spread(self) -> float:
        return abs(self.ask - self.bid)

@dataclass(frozen=True)
class MarketScheduleItem:
    id: int
    status: str
    previousStatus: str
    nextWorking: str  
    nextClosing: str  

    @property
    def is_tradable(self) -> bool:
        """Helper to check if the market is currently active."""
        return self.status.upper() in ("OPEN", "OVERNIGHT")
    
@dataclass(frozen=True)
class ScheduleBatchModel:
    count: int
    items: List[MarketScheduleItem]
    # This allows O(1) lookup: self.lookup[market_id]
    lookup: Dict[int, MarketScheduleItem] 
    type: str = "schedule_batch"

@dataclass(frozen=True)
class PositionModel:
    id: str           # Maps from positionId
    symbol: str       # Maps from code (e.g., #NQJUN26)
    quantity: float
    averagePrice: float
    value: float
    margin: float
    ppl: float
    fxFee: float
    interest: float
    created: str      # ISO Timestamp string
    
    @property
    def side(self) -> str:
        """Determines if the position is BUY (Long) or SELL (Short)."""
        return "SELL" if self.quantity < 0 else "BUY"

@dataclass(frozen=True)
class AccountModel:
    total: float
    free: float
    margin: float
    ppl: float        # Portfolio Profit/Loss
    result: float
    # Trade Counts
    open_trades_count: int = 0
    pending_orders_count: int = 0
    # Updated to hold a list of PositionModel objects
    open_items: List[PositionModel] = field(default_factory=list)
    type: str = "account"

# A type alias for easier type checking in your views
WSModel = Union[TickerModel, ScheduleBatchModel, AccountModel, Dict[str, Any]]