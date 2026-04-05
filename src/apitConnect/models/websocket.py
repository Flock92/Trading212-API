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

@dataclass(frozen=True)
class MarketScheduleItem:
    id: int
    status: str
    previousStatus: str
    nextWorking: str  # ISO Timestamp
    nextClosing: str  # ISO Timestamp

@dataclass(frozen=True)
class ScheduleBatchModel:
    count: int
    items: List[MarketScheduleItem]
    type: str = "schedule_batch"

@dataclass(frozen=True)
class PositionModel:
    id: str
    symbol: str
    quantity: float
    averagePrice: float
    currentPrice: float
    ppl: float

@dataclass(frozen=True)
class AccountModel:
    balance: float
    equity: float
    positions: List[PositionModel] = field(default_factory=list)
    type: str = "account"

# A type alias for easier type checking in your views
WSModel = Union[TickerModel, ScheduleBatchModel, AccountModel, Dict[str, Any]]