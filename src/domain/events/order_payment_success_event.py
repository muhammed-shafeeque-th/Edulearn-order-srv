from typing import Any, Dict, Type, TypeVar
from pydantic import BaseModel, Field, ValidationError, field_validator
from datetime import datetime
from .base_event_dto import BaseEventDto

T = TypeVar("T", bound="OrderPaymentSuccessEventDto")

class OrderPaymentSuccessPayload(BaseModel):
    order_id: str = Field(..., description="ID of the payment is required")
    payment_id: str = Field(..., description="Payment Id of the payment is required")
    user_id: str = Field(..., description="User Id of the payment is required")
    provider: str = Field(..., description="Provider of the payment is required")
    provider_order_id: str = Field(..., description="Provider order Id  of the payment is required")
    payment_status: str = Field(..., description="status of the payment is required")

class OrderPaymentSuccessEventDto(BaseEventDto[OrderPaymentSuccessPayload]):
    @classmethod
    def from_payload(cls: Type[T], event: Dict[str, Any]) -> T:
        payload_data = event.get("payload", {})
        if not isinstance(payload_data, dict):
            raise ValueError("Event payload must be a dictionary.")

        try:
            payload_obj = OrderPaymentSuccessPayload(
                order_id=payload_data["orderId"],
                payment_id=payload_data["paymentId"],
                user_id=payload_data["userId"],
                provider=payload_data["provider"],
                provider_order_id=payload_data["providerOrderId"],
                payment_status=payload_data["paymentStatus"]
            )
        except KeyError as e:
            raise ValueError(f"Missing required payload field: {e}")
        except ValidationError as e:
            raise ValueError(f"Invalid payload data: {e}")

        try:
            timestamp = int(event["timestamp"])
            event_id = str(event["eventId"])
            event_type = str(event["eventType"])
            source = str(event["source"])
        except KeyError as e:
            raise ValueError(f"Missing required event field: {e}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid event field type: {e}")
        
        return cls(
            timestamp=timestamp,
            event_id=event_id,
            event_type=event_type,
            payload=payload_obj,
            source=source,
        )
