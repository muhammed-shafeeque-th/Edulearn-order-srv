"""
Mapping utilities for converting between domain entities and database models.
"""
from typing import List, Optional
from uuid import uuid4

from src.domain.entities.order import Order
from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails
from src.domain.entities.session_booking import SessionBooking

from src.infrastructure.database.models.order_mode import (
    OrderModel, 
    OrderItemModel, 
    PaymentDetailsModel
)
from src.infrastructure.database.models.session_booking_model import SessionBookingModel


class DomainModelMapper:
    """Utility class for mapping between domain entities and database models."""
    
    @staticmethod
    def order_to_model(order: Order) -> OrderModel:
        """Convert Order domain entity to OrderModel."""
        return OrderModel(
            id=order.id,
            user_id=order.user_id,
            amount=order.amount.amount,
            currency=order.amount.currency,
            discount=order.discount,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
    
    @staticmethod
    def order_from_model(order_model: OrderModel) -> Order:
        """Convert OrderModel to Order domain entity."""
        # Convert order items
        items = [DomainModelMapper.orderitem_from_model(item_model) for item_model in order_model.items]
        
        # Convert payment details if exists
        payment_details = None
        if order_model.payment_details:
            payment_details = DomainModelMapper.paymentdetails_from_model(order_model.payment_details)
        
        # Create Money value object
        from src.domain.value_objects.money import Money
        amount = Money(amount=order_model.amount, currency=order_model.currency)
        
        return Order(
            id=order_model.id,
            user_id=order_model.user_id,
            items=items,
            amount=amount,
            discount=order_model.discount,
            status=order_model.status,
            payment_details=payment_details,
            created_at=order_model.created_at,
            updated_at=order_model.updated_at,
        )
    
    @staticmethod
    def orderitem_to_model(order_item: OrderItem, order_id: str) -> OrderItemModel:
        """Convert OrderItem domain entity to OrderItemModel."""
        return OrderItemModel(
            id=str(uuid4()),
            order_id=order_id,
            course_id=order_item.course_id,
            price=order_item.price
        )
    
    @staticmethod
    def orderitem_from_model(order_item_model: OrderItemModel) -> OrderItem:
        """Convert OrderItemModel to OrderItem domain entity."""
        return OrderItem(
            course_id=order_item_model.course_id,
            price=order_item_model.price
        )
    
    @staticmethod
    def paymentdetails_to_model(payment_details: PaymentDetails, order_id: str) -> PaymentDetailsModel:
        """Convert PaymentDetails domain entity to PaymentDetailsModel."""
        return PaymentDetailsModel(
            id=str(uuid4()),
            order_id=order_id,
            payment_id=payment_details.payment_id,
            provider=payment_details.provider,
            provider_order_id=payment_details.provider_order_id,
            payment_status=payment_details.payment_status,
            updated_at=payment_details.updated_at
        )
    
    @staticmethod
    def paymentdetails_from_model(payment_details_model: PaymentDetailsModel) -> PaymentDetails:
        """Convert PaymentDetailsModel to PaymentDetails domain entity."""
        return PaymentDetails(
            payment_id=payment_details_model.payment_id,
            provider=payment_details_model.provider,
            provider_order_id=payment_details_model.provider_order_id,
            payment_status=payment_details_model.payment_status,
            updated_at=payment_details_model.updated_at
        )
    
    @staticmethod
    def sessionbooking_to_model(session_booking: SessionBooking) -> SessionBookingModel:
        """Convert SessionBooking domain entity to SessionBookingModel."""
        return SessionBookingModel(
            id=session_booking.id,
            user_id=session_booking.user_id,
            session_id=session_booking.session_id,
            amount=session_booking.amount.amount,
            currency=session_booking.amount.currency,
            status=session_booking.status,
            created_at=session_booking.created_at,
            updated_at=session_booking.updated_at,
            version=session_booking.version,
        )
    
    @staticmethod
    def sessionbooking_from_model(session_booking_model: SessionBookingModel) -> SessionBooking:
        """Convert SessionBookingModel to SessionBooking domain entity."""
        from src.domain.value_objects.money import Money
        
        return SessionBooking(
            id=session_booking_model.id,
            user_id=session_booking_model.user_id,
            session_id=session_booking_model.session_id,
            amount=Money(amount=session_booking_model.amount, currency=session_booking_model.currency),
            status=session_booking_model.status,
            created_at=session_booking_model.created_at,
            updated_at=session_booking_model.updated_at,
            version=session_booking_model.version,
        )


# Convenience functions for backward compatibility and ease of use
def to_model(entity) -> any:
    """Convenience function to convert any domain entity to its corresponding model."""
    if isinstance(entity, Order):
        return DomainModelMapper.order_to_model(entity)
    elif isinstance(entity, SessionBooking):
        return DomainModelMapper.sessionbooking_to_model(entity)
    elif isinstance(entity, OrderItem):
        raise ValueError("OrderItem requires order_id parameter. Use orderitem_to_model() instead.")
    elif isinstance(entity, PaymentDetails):
        raise ValueError("PaymentDetails requires order_id parameter. Use paymentdetails_to_model() instead.")
    else:
        raise ValueError(f"Unknown entity type: {type(entity)}")


def from_model(model) -> any:
    """Convenience function to convert any database model to its corresponding domain entity."""
    if isinstance(model, OrderModel):
        return DomainModelMapper.order_from_model(model)
    elif isinstance(model, SessionBookingModel):
        return DomainModelMapper.sessionbooking_from_model(model)
    elif isinstance(model, OrderItemModel):
        return DomainModelMapper.orderitem_from_model(model)
    elif isinstance(model, PaymentDetailsModel):
        return DomainModelMapper.paymentdetails_from_model(model)
    else:
        raise ValueError(f"Unknown model type: {type(model)}")
