from abc import ABC, abstractmethod
from fastavro.types import Schema

from typing import TypeVar, Generic

T = TypeVar("T")

class IKafkaProducer(ABC, Generic[T]):
    @abstractmethod
    async def publish_event(self, topic: str, event: T, schema: Schema | None) -> None:
        pass
    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
        
        