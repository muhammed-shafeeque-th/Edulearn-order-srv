from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class RestoreOrderDto(BaseModel):
    order_id: str = Field(..., description="ID of the order is required")
    user_id: str = Field(..., description="ID of the user is required")

