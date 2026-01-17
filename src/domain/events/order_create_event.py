
from dataclasses import dataclass, field
from  datetime import datetime, timezone
from typing import TypedDict, List, Dict, Any
from uuid import uuid4

from src.domain.events.base_event import BaseEvent

class OrderItem(TypedDict):
    course_id: str
    price: float

class OrderCreateEventType(BaseEvent, TypedDict):
    orderId: str
    userId: str
    items: List[OrderItem]
    amount: float
    currency: str

@dataclass
class OrderCreateEvent:
    orderId: str
    userId: str
    items: List[OrderItem]
    amount: float
    currency: str
    eventId: str = field(default_factory=lambda: str(uuid4()))
    eventType: str = field(init=False, default="COURSE_ORDER_CREATE")
    timestamp: int = field(default_factory=lambda: int(datetime.now(timezone.utc).timestamp() * 1000))

    def to_dict(self) -> OrderCreateEventType:
        return {
            "orderId": self.orderId,
            "userId": self.userId,
            "items": self.items,
            "amount": self.amount,
            "currency": self.currency,
            "eventId": self.eventId,
            "eventType": self.eventType,
            "timestamp": self.timestamp,
        }
