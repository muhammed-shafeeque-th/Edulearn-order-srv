
from typing import TypedDict, TypeVar, Generic

T = TypeVar("T")

class BaseEvenType(TypedDict):
    eventId: str
    eventType: str
    timestamp: int
    source: str | None
    eventVersion: str | None

class BaseEvent(TypedDict, Generic[T]):
    eventId: str
    eventType: str
    timestamp: int
    source: str | None
    eventVersion: str | None
    payload: T
