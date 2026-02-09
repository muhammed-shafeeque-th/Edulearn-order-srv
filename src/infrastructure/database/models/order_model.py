from sqlalchemy import Column, Index, String, Float, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.ext.declarative import declarative_base

from src.application.dtos.order_dto import OrderDto
from src.domain.entities.order import Order, OrderStatus
from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails
from src.domain.value_objects.money import Money
from src.infrastructure.database.database import Base

from typing import TypeVar, cast

T = TypeVar("T")


def cast_as(value: T, target_type: type[T]) -> T:
    """
    Casts a value to a specified type.
    """
    return value


class OrderItemModel(Base):
    __tablename__ = "order_items"

    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    course_id = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Relationship back to order
    order = relationship("OrderModel", back_populates="items")

    # Indexes
    __table_args__ = (
        Index("idx_order_items_order_id", "order_id"),
        Index("idx_order_items_course_id", "course_id"),
    )

    # def map_to_domain(self) -> OrderItem:
    #     return OrderItem(
    #         id=self.__dict__["id"],
    #         course_id=self.__dict__['course_id'],
    #         price=self.__dict__['price']
    #     )

    # @classmethod
    # def from_domain(cls, order_item: OrderItem, order_id: str) -> "OrderItemModel":
    #     return cls(
    #         id=str(uuid4()),
    #         order_id=order_id,
    #         course_id=order_item.course_id,
    #         price=order_item.price
    #     )


class PaymentDetailsModel(Base):
    __tablename__ = "payment_details"

    id = Column(String, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"),
                      nullable=False, unique=True)
    payment_id = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    provider_order_id = Column(String, nullable=False)
    payment_status = Column(String, default="pending")
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationship back to order
    order = relationship(
        "OrderModel", back_populates="payment_details", uselist=False)

    # Indexes
    __table_args__ = (
        Index("idx_payment_details_order_id", "order_id"),
        Index("idx_payment_details_payment_id", "payment_id"),
        Index("idx_payment_details_provider_order_id", "provider_order_id"),
    )

    # def map_to_domain(self) -> PaymentDetails:
    #     return PaymentDetails(
    #         id=self.__dict__["id"],
    #         payment_id=self.__dict__["payment_id"],
    #         provider=self.__dict__["provider"],
    #         provider_order_id=self.__dict__["provider_order_id"],
    #         payment_status=self.__dict__["payment_status"],
    #         updated_at=self.__dict__["updated_at"]
    #     )

    # @classmethod
    # def from_domain(cls, pd: PaymentDetails, order_id: str):
    #     return cls(
    #         id=str(uuid4()) if not getattr(pd, "id", None) else pd.id,
    #         order_id=order_id,
    #         payment_id=pd.payment_id,
    #         provider=pd.provider,
    #         provider_order_id=pd.provider_order_id,
    #         payment_status=pd.payment_status,
    #         updated_at=pd.updated_at or datetime.utcnow()
    #     )


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, index=True)
    idempotency_key = Column(String, unique=True, index=True, nullable=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    sub_total = Column(Integer, default=0, nullable=False)
    sales_tax = Column(Integer, default=0, nullable=False)
    discount = Column(Integer, nullable=True)
    status = Column(String, default="PENDING")
    created_at = Column(DateTime(timezone=True),
                        default=datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

   # Use selectin loading to avoid lazy sync IO
    items = relationship(
        "OrderItemModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    payment_details = relationship(
        "PaymentDetailsModel",
        back_populates="order",
        uselist=False,
        lazy="selectin"
    )

    # Indexes for common queries
    __table_args__ = (
        Index("idx_orders_user_id", "user_id"),
        Index("idx_orders_status", "status"),
    )
    
    # def map_to_domain(self) -> Order:
    #     # Convert order items
    #     items = [item_model.map_to_domain() for item_model in self.items]

    #     # Convert payment details if exists
    #     payment_details = None
    #     if self.payment_details:
    #         payment_details = self.payment_details.map_to_domain()

    #     # Create Money value object
    #     amount = Money(amount=self.__dict__[
    #                          "amount"], currency=self.__dict__["currency"])

    #     return Order(
    #         id=self.__dict__["id"],
    #         user_id=self.__dict__["user_id"],
    #         idempotency_key=self.__dict__["idempotency_key"],
    #         # course_ids=list(self.__dict__["course_ids"]) if self.__dict__["course_ids"] else [],
    #         items=items,
    #         sales_tax=self.__dict__["sales_tax"],
    #         amount=amount,
    #         sub_total=self.__dict__['sub_total'],
    #         discount=self.__dict__['discount'],
    #         status=OrderStatus(self.__dict__["status"]),
    #         payment_details=payment_details,
    #         created_at=self.__dict__["created_at"],
    #         updated_at=self.__dict__["updated_at"],
    #     )

    # @classmethod
    # def from_domain(cls, order: Order) -> "OrderModel":
    #     return cls(
    #         id=order.id,
    #         user_id=order.user_id,
    #         idempotency_key=order.idempotency_key,
    #         amount=order.amount.amount,
    #         currency=order.amount.currency,
    #         discount=order.discount,
    #         sales_tax=order.sales_tax,
    #         status=order.status.value,
    #         created_at=order.created_at,
    #         updated_at=order.updated_at,
    #     )
