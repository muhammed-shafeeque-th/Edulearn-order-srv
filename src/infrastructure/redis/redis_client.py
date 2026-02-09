import json
from typing import Any, Optional
# import redis
from redis.asyncio import ConnectionPool, Redis
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.redis_interface import IRedisService
from src.infrastructure.config.settings import settings
from contextlib import asynccontextmanager


# class RedisLock:
#     def __init__(self, lock):
#         self.lock = lock

#     async def __aenter__(self):
#         await self.lock.acquire()
#         return self.lock

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         await self.lock.release()

class RedisClient(IRedisService):
    def __init__(self, logger_service: ILoggingService):
        self.logger = logger_service.get_logger("RedisClient")
        self.key_prefix = settings.REDIS_KEY_PREFIX
        self.pool = ConnectionPool.from_url(
            settings.REDIS_URL,
            max_connections=50,
            decode_responses=True,
            retry_on_timeout=True,
            socket_timeout=5,
            socket_connect_timeout=5,
        )
        self._client: Redis = Redis.from_pool(self.pool)

    @asynccontextmanager
    async def lock(self, key: str, timeout: int = 10):
        lock = self._client.lock(self.key_prefix + key, timeout=timeout)
        try:
            await lock.acquire()
            yield lock
        finally:
            await lock.release()

    async def get(self, key: str) -> Optional[bytes]:
        try:
            value = await self._client.get(self.key_prefix + key)
            self.logger.debug(f"Redis get: {key} -> {value}")
            return value
        except Exception as e:
            self.logger.error(f"Redis get failed for key {key}: {str(e)}")
            raise

    async def delete(self, key: str) -> None:
        try:
            await self._client.delete(self.key_prefix + key)
            self.logger.debug(f"Redis delete: {key}")
        except Exception as e:
            self.logger.error(f"Redis delete failed for key {key}: {str(e)}")
            raise
        
    async def delete_pattern(self, key: str) -> None:
        """
        Deletes all keys matching the given pattern (after applying key_prefix).
        """
        pattern = self.key_prefix + key
        try:
            async for k in self._client.scan_iter(match=pattern):
                await self._client.delete(k)
                self.logger.debug(f"Redis delete_pattern: deleted {k}")
        except Exception as e:
            self.logger.error(f"Redis delete_pattern failed for pattern {pattern}: {str(e)}")
            raise

    async def set(self, key: str, value: Any, expire: int | None = settings.REDIS_TTL) -> None:
        try:
            if isinstance(value, (str, bytes)):
                await self._client.set(self.key_prefix + key, value, ex=expire or settings.REDIS_TTL)
            else:
                await self._client.set(self.key_prefix + key, json.dumps(value), ex=expire or settings.REDIS_TTL)
            self.logger.debug(f"Redis set: {key} -> {value}")
        except Exception as e:
            self.logger.error(f"Redis set failed for key {key}: {str(e)}")
            raise

    async def close(self):
        await self._client.close()
        await self.pool.disconnect()

    @property
    def client(self) -> Redis:
        return self._client


# redis_client = RedisClient(logging)
