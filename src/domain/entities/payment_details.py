from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Any

# Define valid payment status transitions
PaymentStatus = Literal["pending", "success", "failed", "refunded", "expired"]

# class PaymentStatus(str, Enum):
#     PENDING = "pending"
#     PENDING = "pending"
#     SUCCESS = "success"
#     FAILED = "failed"
#     REFUNDED = "refunded"
#     EXPIRED = "expired"

_PAYMENT_LIFECYCLE = {
    "pending": {"success", "failed", "expired"},
    "success": {"refunded"},
    "failed": set(),
    "refunded": set(),
    "expired": set(),
}


class PaymentLifecycleException(Exception):
    pass


@dataclass
class PaymentDetails:
    id: str
    payment_id: str
    provider: str
    provider_order_id: str
    payment_status: PaymentStatus = "pending"
    updated_at: datetime = datetime.now()

    @classmethod
    def create(
        cls,
        id: str,
        payment_id: str,
        provider: str,
        provider_order_id: str,
        payment_status: PaymentStatus = "pending"
    ) -> "PaymentDetails":
        return cls(
            id,
            payment_id,
            provider,
            provider_order_id,
            payment_status,
        )

    def _validate_transition(self, new_status: PaymentStatus):
        allowed = _PAYMENT_LIFECYCLE.get(self.payment_status, set())
        if new_status not in allowed:
            raise PaymentLifecycleException(
                f"Invalid payment status transition from {self.payment_status} to {new_status}"
            )

    def mark_success(self) -> None:
        self._validate_transition("success")
        self.payment_status = "success"
        self.updated_at = datetime.now()

    def mark_failed(self) -> None:
        self._validate_transition("failed")
        self.payment_status = "failed"
        self.updated_at = datetime.now()

    def mark_refunded(self) -> None:
        self._validate_transition("refunded")
        self.payment_status = "refunded"
        self.updated_at = datetime.now()

    def mark_expired(self) -> None:
        self._validate_transition("expired")
        self.payment_status = "expired"
        self.updated_at = datetime.now()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "payment_id": self.payment_id,
            "provider": self.provider,
            "provider_order_id": self.provider_order_id,
            "payment_status": self.payment_status,
            "updated_at": self.updated_at,
        }
