
from typing import TypedDict, List
from dataclasses import dataclass, field
from datetime import datetime, timezone
from src.domain.events.base_event_type import BaseEvent
from uuid import uuid4


class OrderItem(TypedDict):
    courseId: str
    price: float


class OrderCreatedEventPayload(TypedDict):
    orderId: str
    userId: str
    items: List[OrderItem]
    subtotal: int
    discount: int
    couponDiscount: int
    tax: int
    total: int
    currency: str


class OrderCreatedEventType(BaseEvent[OrderCreatedEventPayload]):
    pass


@dataclass
class OrderCreatedEvent:
    orderId: str
    userId: str
    items: List[OrderItem]
    subtotal: int
    discount: int
    coupon_discount: int
    tax: int
    total: int
    currency: str
    eventId: str = field(default_factory=lambda: str(uuid4()))
    eventType: str = field(init=False, default="CourseOrderCreated")
    timestamp: int = field(default_factory=lambda: int(
        datetime.now(timezone.utc).timestamp() * 1000))

    def to_dict(self) -> OrderCreatedEventType:
        return {
            "payload": {
                "orderId": self.orderId,
                "userId": self.userId,
                "items": self.items,
                "subtotal": self.subtotal,
                "discount": self.discount,
                "couponDiscount": self.coupon_discount,
                "tax": self.tax,
                "total": self.total,
                "currency": self.currency,
            },

            "eventId": self.eventId,
            "eventType": self.eventType,
            "timestamp": self.timestamp,
            "eventVersion": "0.0.1",
            "source": "order-service"
        }
