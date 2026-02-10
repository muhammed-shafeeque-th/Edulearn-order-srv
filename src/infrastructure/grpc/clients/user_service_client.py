import grpc
from grpc import aio

from src.infrastructure.config.settings import settings
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.grpc_client_interface import IUserServiceClient
from src.infrastructure.grpc.interceptors.client_inerceptors import ClientAuthInterceptor, ClientTracingInterceptor
from ..generated.user_service_pb2 import GetUserRequest
from ..generated.user_service_pb2_grpc import UserServiceStub
from src.infrastructure.grpc.clients.channel_pool import ChannelPool
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit


class UserServiceClient(IUserServiceClient):
    def __init__(self, logging_service: ILoggingService, token: str | None = None):
        self.pool = ChannelPool(settings.USER_SERVICE_NAME, settings.USER_SERVICE_GRPC,
                                logging_service=logging_service, max_size=10)
        self.logger = logging_service.get_logger("UserServiceClient")
        self.interceptors = [
            ClientTracingInterceptor(),
            # ClientAuthInterceptor(token) if token else None,
        ]
        self.interceptors = [i for i in self.interceptors if i is not None]

    @circuit(failure_threshold=5, recovery_timeout=30)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get_user(self, user_id: str) -> dict:
        channel = await self.pool.acquire()
        try:
            from typing import Any, cast
            intercept_fn = getattr(aio, "intercept_channel", None)
            if callable(intercept_fn):
                intercepted = cast(Any, intercept_fn)(
                    channel, *self.interceptors)
            else:
                intercepted = channel
            stub = UserServiceStub(intercepted)
            request = GetUserRequest(userId=user_id)
            response = await stub.GetUser(request)
            has_error = False
            if hasattr(response, "HasField"):
                try:
                    # type: ignore[attr-defined]
                    has_error = response.HasField("error")
                except Exception:
                    has_error = False
            else:
                err = getattr(response, "error", None)
                err_code = getattr(err, "code", "") if err is not None else ""
                err_msg = getattr(
                    err, "message", "") if err is not None else ""
                has_error = bool(err_code or err_msg)

            if has_error:
                err = getattr(response, "error", None)
                self.logger.error(
                    f"Failed to fetch user with Id {user_id}: {getattr(err, 'message', '')}")
                raise ValueError(getattr(err, "message", "Unknown error"))

            return {"user_id": getattr(response, "id", None), "role": getattr(response, "role", None)}
        except Exception as e:
            self.logger.error(f"Failed to verify user {user_id}: {str(e)}")
            raise
        finally:
            await self.pool.release(channel)

    async def close(self):
        await self.pool.close()
