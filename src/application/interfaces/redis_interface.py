from abc import ABC, abstractmethod
from typing import Optional, Any, AsyncContextManager

from redis.asyncio import client

class IRedisService(ABC):
    @property
    @abstractmethod
    def client(self) -> client.Redis:
        pass
    
    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, expire: int | None) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass
    
    @abstractmethod
    async def delete_pattern(self, key: str) -> None:
        pass

    @abstractmethod
    def lock(self, key: str, timeout: int = 10) -> AsyncContextManager:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
    
    
    