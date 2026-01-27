
from typing import TypedDict, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
from src.domain.events.base_event_type import BaseEvent
from uuid import uuid4


class OrderItem(TypedDict):
    courseId: str
    price: float


class OrderSucceededEventPayload(TypedDict):
    orderId: str
    userId: str
    items: List[OrderItem]
    amount: float
    currency: str


class OrderSucceededEventType(BaseEvent[OrderSucceededEventPayload]):
    pass


@dataclass
class OrderSucceededEvent:
    orderId: str
    userId: str
    items: List[OrderItem]
    amount: float
    currency: str
    eventId: str = field(default_factory=lambda: str(uuid4()))
    eventType: str = field(init=False, default="CourseOrderSucceeded")
    timestamp: int = field(default_factory=lambda: int(
        datetime.now(timezone.utc).timestamp() * 1000))

    def to_dict(self) -> OrderSucceededEventType:
        return {
            "payload": {
                "orderId": self.orderId,
                "userId": self.userId,
                "items": self.items,
                "amount": self.amount,
                "currency": self.currency,
            },

            "eventId": self.eventId,
            "eventType": self.eventType,
            "timestamp": self.timestamp,
            "eventVersion": "0.0.1",
            "source": "order-service"
        }
