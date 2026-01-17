from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class BaseEventTypeDto(BaseModel):
    event_id: str = Field(..., description="ID of the event is required")
    event_type: str = Field(..., description="Event type of the event is required")
    timestamp: int = Field(..., description="timestamp  of the payment is required")