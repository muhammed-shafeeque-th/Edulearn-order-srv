
from dataclasses import dataclass, field
from typing import TypedDict, List
from datetime import datetime, timezone
from uuid import uuid4

from src.domain.events.base_event_type import BaseEvent


class OrderItem(TypedDict):
    courseId: str
    price: float


class OrderFailedEventPayload(TypedDict):
    orderId: str
    userId: str
    items: List[OrderItem]
    amount: float
    currency: str


class OrderFailedEventType(BaseEvent[OrderFailedEventPayload]):
    pass


@dataclass
class OrderFailedEvent:
    orderId: str
    userId: str
    items: List[OrderItem]
    amount: float
    currency: str
    eventId: str = field(default_factory=lambda: str(uuid4()))
    eventType: str = field(init=False, default="CourseOrderFailed")
    timestamp: int = field(default_factory=lambda: int(
        datetime.now(timezone.utc).timestamp() * 1000))

    def to_dict(self) -> OrderFailedEventType:
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
