from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Literal
from uuid import uuid4

from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails
from src.domain.value_objects.money import Money


class OrderLifecycleException(Exception):
    pass


class OrderStatus(Enum):
    CREATED = 'created'
    PENDING_PAYMENT = 'pending_payment'
    PROCESSING = 'processing'
    SUCCEEDED = 'succeeded'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    REFUNDED = 'refunded'
    EXPIRED = 'expired'


# Allowed transitions for each state
_ORDER_LIFECYCLE = {
    OrderStatus.CREATED: {
        OrderStatus.PENDING_PAYMENT,
        OrderStatus.CANCELLED,
        OrderStatus.EXPIRED,
    },
    OrderStatus.PENDING_PAYMENT: {
        OrderStatus.PROCESSING,
        OrderStatus.CANCELLED,
        OrderStatus.FAILED,
        OrderStatus.EXPIRED,
    },
    OrderStatus.PROCESSING: {
        OrderStatus.SUCCEEDED,
        OrderStatus.FAILED,
        OrderStatus.CANCELLED,
    },
    OrderStatus.SUCCEEDED: {
        OrderStatus.REFUNDED,
    },
    OrderStatus.FAILED: {},
    OrderStatus.CANCELLED: {},
    OrderStatus.REFUNDED: {},
    OrderStatus.EXPIRED: {},
}


@dataclass
class Order:
    id: str
    user_id: str
    idempotency_key: str | None
    items: list[OrderItem]
    amount: Money
    sub_total: float
    sales_tax: float
    discount: float | None
    status: OrderStatus
    payment_details: PaymentDetails | None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        user_id: str,
        idempotency_key: str | None,
        items: list[OrderItem],
        amount: Money,
        discount: float | None,
        sub_total: float,
        sales_tax: float,
        payment_details: PaymentDetails | None,
        status: OrderStatus = OrderStatus.CREATED,
    ) -> "Order":
        if not items or len(items) == 0:
            raise ValueError("Order must have at least one item.")
        if discount is not None and discount < 0:
            raise ValueError("Discount cannot be negative")
        if sub_total < 0 or sales_tax < 0:
            raise ValueError("Sub_total and sales_tax must be non-negative")
        if any(item.price < 0 for item in items):
            raise ValueError("Item prices must be non-negative")
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            idempotency_key=idempotency_key,
            items=items,
            amount=amount,
            sub_total=sub_total,
            sales_tax=sales_tax,
            discount=discount,
            status=status,
            payment_details=payment_details,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    def _validate_transition(self, new_status: OrderStatus) -> None:
        allowed = _ORDER_LIFECYCLE.get(self.status, set())
        if new_status not in allowed:
            raise OrderLifecycleException(
                f"Invalid order status transition from {self.status.value} to {new_status.value}"
            )

    def mark_pending_payment(self) -> None:
        self._validate_transition(OrderStatus.PENDING_PAYMENT)
        self.status = OrderStatus.PENDING_PAYMENT
        self.updated_at = datetime.now(timezone.utc)

    def mark_processing(self) -> None:
        self._validate_transition(OrderStatus.PROCESSING)
        self.status = OrderStatus.PROCESSING
        self.updated_at = datetime.now(timezone.utc)

    def mark_completed(self) -> None:
        self._validate_transition(OrderStatus.SUCCEEDED)
        self.status = OrderStatus.SUCCEEDED
        self.updated_at = datetime.now(timezone.utc)

    def mark_failed(self) -> None:
        self._validate_transition(OrderStatus.FAILED)
        self.status = OrderStatus.FAILED
        self.updated_at = datetime.now(timezone.utc)

    def mark_cancelled(self) -> None:
        self._validate_transition(OrderStatus.CANCELLED)
        self.status = OrderStatus.CANCELLED
        self.updated_at = datetime.now(timezone.utc)

    def mark_refunded(self) -> None:
        self._validate_transition(OrderStatus.REFUNDED)
        self.status = OrderStatus.REFUNDED
        self.updated_at = datetime.now(timezone.utc)

    def mark_expired(self) -> None:
        self._validate_transition(OrderStatus.EXPIRED)
        self.status = OrderStatus.EXPIRED
        self.updated_at = datetime.now(timezone.utc)

    def add_item(self, item: OrderItem) -> None:
        # Don't allow adding items if the order is finalized
        if self.status in {
            OrderStatus.SUCCEEDED,
            OrderStatus.FAILED,
            OrderStatus.CANCELLED,
            OrderStatus.REFUNDED,
            OrderStatus.EXPIRED,
        }:
            raise OrderLifecycleException(
                f"Cannot add items to order in '{self.status.value}' state"
            )
        if item.price < 0:
            raise ValueError("Item price cannot be negative")
        self.items.append(item)
        self.recalculate_total()
        self.updated_at = datetime.now(timezone.utc)

    def add_items(self, items: list[OrderItem]) -> None:
        if self.status in {
            OrderStatus.SUCCEEDED,
            OrderStatus.FAILED,
            OrderStatus.CANCELLED,
            OrderStatus.REFUNDED,
            OrderStatus.EXPIRED,
        }:
            raise OrderLifecycleException(
                f"Cannot add items to order in '{self.status.value}' state"
            )
        if not items:
            raise ValueError("No items provided")
        if any(item.price < 0 for item in items):
            raise ValueError("Item prices must be non-negative")
        self.items.extend(items)
        self.recalculate_total()
        self.updated_at = datetime.now(timezone.utc)

    def set_discount(self, discount: int | None) -> None:
        if self.status in {
            OrderStatus.SUCCEEDED,
            OrderStatus.FAILED,
            OrderStatus.CANCELLED,
            OrderStatus.REFUNDED,
            OrderStatus.EXPIRED,
        }:
            raise OrderLifecycleException(
                f"Cannot set discount for order in '{self.status.value}' state"
            )
        if discount is not None and discount < 0:
            raise ValueError("Discount cannot be negative")
        self.discount = discount
        self.recalculate_total()
        self.updated_at = datetime.now(timezone.utc)

    def set_payment_details(self, payment_details: PaymentDetails | None) -> None:
        if self.status in {
            OrderStatus.CANCELLED,
            OrderStatus.REFUNDED,
            OrderStatus.FAILED,
            OrderStatus.EXPIRED,
        }:
            raise OrderLifecycleException(
                f"Cannot set payment details for order in '{self.status.value}' state"
            )
        self.payment_details = payment_details
        self.updated_at = datetime.now(timezone.utc)

    def recalculate_total(self) -> None:
        base_total = float(sum(item.price for item in self.items))
        if self.discount is not None and self.discount > 0:
            # Interpret discount as a flat amount in same currency units
            base_total = max(0.0, base_total - float(self.discount))
        self.amount = Money(amount=base_total, currency=self.amount.currency)

    def reset(self) -> None:
        """
        Reset the order state in case payment needs to be retried after failure/cancellation/expiration.
        """
        # if self.status not in {OrderStatus.FAILED, OrderStatus.CANCELLED, OrderStatus.EXPIRED}:
        #     raise OrderLifecycleException(
        #         f"Order can only be reset from FAILED, CANCELLED, or EXPIRED status, current: {self.status.value}")

        self.status = OrderStatus.CREATED
        self.payment_details = None
        self.updated_at = datetime.now(timezone.utc)
