from datetime import datetime
import json
from typing import Any, Optional, List, Dict
from uuid import uuid4
from src.domain.entities.order import Order, OrderStatus
from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails
from src.domain.value_objects.money import Money
from src.infrastructure.database.models.order_model import (
    OrderItemModel,
    OrderModel,
    PaymentDetailsModel,
)


class EntityMapper:
    """Centralized entity mapper for converting between ORM models and domain models."""

    @staticmethod
    def to_domain_order(order_model: OrderModel) -> Order:
        """Converts an OrderModel ORM instance to a domain Order."""
        items = [
            EntityMapper.to_domain_order_item(item)
            for item in getattr(order_model, "items", []) or []
        ]

        payment_details = (
            EntityMapper.to_domain_payment_details(order_model.payment_details)
            if hasattr(order_model, "payment_details") and order_model.payment_details
            else None
        )

        return Order(
            id=getattr(order_model, "id"),
            user_id=getattr(order_model, "user_id"),
            idempotency_key=getattr(order_model, "idempotency_key"),
            amount=Money(
                amount=float(getattr(order_model, "amount")),
                currency=getattr(order_model, "currency"),
            ),
            discount=(
                float(getattr(order_model, "discount"))
                if getattr(order_model, "discount") is not None
                else None
            ),
            sub_total=float(getattr(order_model, "sub_total")) if getattr(
                order_model, "sub_total") is not None else 0,
            sales_tax=float(getattr(order_model, "sales_tax")) if getattr(
                order_model, "sales_tax") is not None else 0,
            status=OrderStatus(getattr(order_model, "status")) if isinstance(
                getattr(order_model, "status"), str) else getattr(order_model, "status"),
            created_at=getattr(order_model, "created_at"),
            updated_at=getattr(order_model, "updated_at"),
            items=items,
            payment_details=payment_details,
        )

    @staticmethod
    def to_orm_order(order: Order) -> OrderModel:
        """Converts a domain Order to an ORM OrderModel."""
        return OrderModel(
            id=order.id,
            user_id=order.user_id,
            idempotency_key=order.idempotency_key,
            amount=order.amount.amount,
            currency=order.amount.currency,
            discount=order.discount,
            sub_total=order.sub_total,
            sales_tax=order.sales_tax,
            status=order.status.value if hasattr(
                order.status, "value") else order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )

    @staticmethod
    def to_domain_order_item(item_model: OrderItemModel) -> OrderItem:
        """Converts an OrderItemModel ORM instance to a domain OrderItem."""
        return OrderItem(
            id=getattr(item_model, "id"),
            course_id=getattr(item_model, "course_id"),
            price=getattr(item_model, "price"),
        )

    @staticmethod
    def to_orm_order_item(order_item: OrderItem, order_id: str) -> OrderItemModel:
        """Converts a domain OrderItem to OrderItemModel ORM instance."""
        return OrderItemModel(
            id=str(uuid4()),
            order_id=order_id,
            course_id=order_item.course_id,
            price=order_item.price,
        )

    @staticmethod
    def to_domain_payment_details(payment_details_model: Optional[PaymentDetailsModel]) -> Optional[PaymentDetails]:
        """Converts a PaymentDetailsModel ORM instance to a domain PaymentDetails."""
        if not payment_details_model:
            return None
        return PaymentDetails(
            id=payment_details_model.__dict__["id"],
            payment_id=payment_details_model.__dict__["payment_id"],
            provider=payment_details_model.__dict__["provider"],
            provider_order_id=payment_details_model.__dict__[
                "provider_order_id"],
            payment_status=payment_details_model.__dict__["payment_status"],
            updated_at=payment_details_model.__dict__["updated_at"],
        )

    @staticmethod
    def to_orm_payment_details(pd: PaymentDetails, order_id: str) -> PaymentDetailsModel:
        """Converts a domain PaymentDetails to ORM PaymentDetailsModel instance."""
        return PaymentDetailsModel(
            id=str(uuid4()) if not getattr(pd, "id", None) else pd.id,
            order_id=order_id,
            payment_id=pd.payment_id,
            provider=pd.provider,
            provider_order_id=pd.provider_order_id,
            payment_status=pd.payment_status,
            updated_at=pd.updated_at or datetime.utcnow(),
        )

    @staticmethod
    def serialize_order_to_json(order: Order) -> str:
        """Serializes a domain Order to a JSON string."""
        return json.dumps({
            "id": order.id,
            "user_id": order.user_id,
            "idempotency_key": order.idempotency_key,
            "items": [
                {
                    "id": i.id,
                    "course_id": i.course_id,
                    "price": i.price,
                } for i in order.items
            ],
            "amount": order.amount.amount,
            "currency": order.amount.currency,
            "discount": order.discount,
            "sub_total": order.sub_total,
            "sales_tax": order.sales_tax,
            "status": order.status.value if hasattr(order.status, "value") else order.status,
            "payment_details": (
                {
                    "id": order.payment_details.id,
                    "payment_id": order.payment_details.payment_id,
                    "provider": order.payment_details.provider,
                    "provider_order_id": order.payment_details.provider_order_id,
                    "payment_status": order.payment_details.payment_status,
                    "updated_at": order.payment_details.updated_at.isoformat()
                    if getattr(order.payment_details, "updated_at", None)
                    else None,
                } if order.payment_details else None
            ),
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "updated_at": order.updated_at.isoformat() if order.updated_at else None,
        })

    @staticmethod
    def deserialize_json_to_order(order_data: Dict[str, Any]) -> Order:
        """Deserializes JSON dict data to a domain Order."""
        items = [
            OrderItem(
                id=item["id"],
                course_id=item["course_id"],
                price=item["price"],
            )
            for item in order_data.get("items", []) or []
        ]

        payment_details = order_data.get("payment_details")
        payment_details_obj = None
        if payment_details:
            payment_details_obj = PaymentDetails(
                id=payment_details.get("id"),
                payment_id=payment_details.get("payment_id"),
                provider=payment_details.get("provider"),
                provider_order_id=payment_details.get("provider_order_id"),
                payment_status=payment_details.get(
                    "payment_status", "pending"),
                updated_at=datetime.fromisoformat(
                    payment_details["updated_at"]) if payment_details.get("updated_at") else datetime.now(),
            )

        return Order(
            id=order_data["id"],
            user_id=order_data["user_id"],
            idempotency_key=order_data.get("idempotency_key"),
            items=items,
            amount=Money(
                amount=order_data["amount"],
                currency=order_data["currency"]
            ),
            sub_total=order_data.get("sub_total", 0),
            sales_tax=order_data.get("sales_tax", 0),
            discount=order_data.get("discount"),
            status=order_data["status"] if isinstance(
                order_data["status"], OrderStatus) else OrderStatus(order_data["status"]),
            payment_details=payment_details_obj,
            created_at=datetime.fromisoformat(order_data["created_at"]),
            updated_at=datetime.fromisoformat(order_data["updated_at"]),
        )
