from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from datetime import datetime
import uuid


class EventType(Enum):
    PIPELINE = "pipeline"
    API_REQUEST = "api_request"
    API_RESPONSE = "api_response"
    ERROR = "error"
    SYSTEM = "system"


@dataclass
class Event:
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    correlation_id: Optional[uuid.UUID] = None

    type: EventType = EventType.SYSTEM
    message: str = ""

    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    error: Optional[Exception] = None

    @classmethod
    def api_request(cls, message: str, **data):
        corr_id = uuid.uuid4()
        return cls(
            type=EventType.API_REQUEST,
            message=message,
            correlation_id=corr_id,
            data=data
        )

    @classmethod
    def api_response(cls, message: str, correlation_id: uuid.UUID, **data):
        return cls(
            type=EventType.API_RESPONSE,
            message=message,
            correlation_id=correlation_id,
            data=data
        )

    @classmethod
    def pipeline(
        cls,
        message: str,
        raw: Any,
        processed: Optional[Dict[str, Any]] = None,
        correlation_id: Optional[uuid.UUID] = None
    ):
        return cls(
            type=EventType.PIPELINE,
            message=message,
            correlation_id=correlation_id or uuid.uuid4(),
            data={
                "raw": raw,
                "processed": processed
            }
        )

    @classmethod
    def system(cls, message: str, **data):
        return cls(
            type=EventType.SYSTEM,
            message=message,
            data=data
        )

    @classmethod
    def error(cls, message: str, error: Exception, correlation_id: Optional[uuid.UUID] = None, **data):
        return cls(
            type=EventType.ERROR,
            message=message,
            correlation_id=correlation_id,
            data=data,
            error=error
        )