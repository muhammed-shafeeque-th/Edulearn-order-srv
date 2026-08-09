
from src.domain.entities.order import Order
from src.infrastructure.grpc.generated.order_service_pb2 import MoneyData, OrderData, OrderItemsData, PaymentDetailsData


class OrderResponseMapper():
    # class Config:
    #     from_attributes = True

    @classmethod
    def to_grpc_response(cls, order:Order) -> "OrderData":      
        return OrderData(
                    id=order.id,
                    user_id=order.user_id,
                    items=[OrderItemsData(course_id=item.course_id,
                                          price=item.price) for item in order.items],
                    amount=MoneyData(
                        total=order.amount.amount,
                        currency=order.amount.currency,
                        discount=order.discount,
                        sales_tax=order.sales_tax,
                        sub_total=order.sub_total,
                    ),
                    status=order.status.value,
                    payment_details=PaymentDetailsData(
                        payment_status=order.payment_details.payment_status,
                        payment_id=order.payment_details.payment_id,
                        provider=order.payment_details.provider,
                        provider_order_id=order.payment_details.provider_order_id if order.payment_details else None,
                        updated_at=order.payment_details.updated_at.isoformat(
                        ) if order.payment_details else None,
                    ) if order.payment_details else None,
                    created_at=order.created_at.isoformat(),
                    updated_at=order.updated_at.isoformat(),
        
                )

        
