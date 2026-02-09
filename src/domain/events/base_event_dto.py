from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class BaseEventDto(BaseModel, Generic[T]):
    event_id: str = Field(..., description="ID of the event is required")
    event_type: str = Field(..., description="Event type of the event is required")
    timestamp: int = Field(..., description="Timestamp of the event is required")
    source: Optional[str] = Field(default=None, description="Source of the event")
    event_version: Optional[str] = Field(default=None, description="Version of the event")
    payload: T
