from datetime import datetime

from pydantic import BaseModel

from src.domain.entities.order import Order, OrderStatus
from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails
from src.domain.value_objects.money import Money
from src.infrastructure.grpc.generated.order_service_pb2 import MoneyData, OrderData, OrderItemsData, PaymentDetailsData


class OrderDto(BaseModel):
    id: str
    user_id: str
    items: list[OrderItem]
    amount: Money
    discount: float | None
    sub_total: float | None
    sales_tax: float | None
    status: OrderStatus
    payment_details: PaymentDetails | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_domain(cls, order: Order) -> "OrderDto":
      
        return cls(
            id=order.id,
            user_id=order.user_id,
            items=order.items,
            sales_tax=order.sales_tax,
            amount=Money(order.amount.amount, order.amount.currency),
            discount=order.discount,
            sub_total=order.sub_total,
            status=order.status,
            payment_details=order.payment_details,
            created_at=order.created_at,
            updated_at=order.updated_at,

        )

    def to_response_data(self) -> "OrderData":
        return OrderData(
            id=self.id,
            user_id=self.user_id,
            items=[OrderItemsData(course_id=item.course_id,
                                  price=item.price) for item in self.items],
            amount=MoneyData(
                total=self.amount.amount,
                currency=self.amount.currency,
                discount=self.discount,
                sales_tax=self.sales_tax,
                sub_total=self.sub_total,
            ),
            status=self.status.value,
            payment_details=PaymentDetailsData(
                payment_status=self.payment_details.payment_status,
                payment_id=self.payment_details.payment_id,
                provider=self.payment_details.provider,
                provider_order_id=self.payment_details.provider_order_id if self.payment_details else None,
                updated_at=self.payment_details.updated_at.isoformat(
                ) if self.payment_details else None,
            ) if self.payment_details else None,
            created_at=self.created_at.isoformat(),
            updated_at=self.updated_at.isoformat(),

        )
