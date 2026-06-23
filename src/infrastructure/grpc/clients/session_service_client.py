import grpc
from grpc import aio

from src.infrastructure.config.settings import settings
from src.application.interfaces.logging_interface import ILoggingService
from src.infrastructure.grpc.interceptors.client_inerceptors import ClientAuthInterceptor, ClientTracingInterceptor
from ..generated.session_service_pb2 import GetSessionRequest, GetAvailableSlotsRequest
from ..generated.session_service_pb2_grpc import SessionServiceStub
from src.application.interfaces.grpc_client_interface import ISessionServiceClient
from src.infrastructure.grpc.clients.channel_pool import ChannelPool
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit


class SessionServiceClient(ISessionServiceClient):
    def __init__(self, logging_service: ILoggingService, token: str | None = None):
        self.pool = ChannelPool(
            settings.SESSION_SERVICE_NAME, settings.SESSION_SERVICE_GRPC, max_size=10, logging_service=logging_service)
        self.logger = logging_service.get_logger("SessionServiceClient")
        self.interceptors = [
            ClientTracingInterceptor(),
            ClientAuthInterceptor(token) if token else None,
        ]
        self.interceptors = [i for i in self.interceptors if i is not None]

    @circuit(failure_threshold=5, recovery_timeout=30)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get_session(self, session_id: str) -> dict:
        channel = await self.pool.acquire()
        try:
            intercepted_channel = grpc.intercept_channel(
                channel, *self.interceptors)
            stub = SessionServiceStub(intercepted_channel)
            request = GetSessionRequest(session_id=session_id)
            response = await stub.GetSession(request)
            if response.error:
                self.logger.error(
                    f"Failed to get session {session_id}: {response.error}")
                raise ValueError(response.error)
            return {"session_id": response.session_id, "price": response.price, "max_slots": response.max_slots}
        except Exception as e:
            self.logger.error(f"Failed to get session {session_id}: {str(e)}")
            raise
        finally:
            await self.pool.release(channel)

    @circuit(failure_threshold=5, recovery_timeout=30)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get_available_slots(self, session_id: str) -> int:
        channel = await self.pool.acquire()
        try:
            intercepted_channel = grpc.intercept_channel(
                channel, *self.interceptors)
            stub = SessionServiceStub(intercepted_channel)
            request = GetAvailableSlotsRequest(session_id=session_id)
            response = await stub.GetAvailableSlots(request)
            if response.error:
                self.logger.error(
                    f"Failed to get available slots for session {session_id}: {response.error}")
                raise ValueError(response.error)
            return response.available_slots
        except Exception as e:
            self.logger.error(
                f"Failed to get available slots for session {session_id}: {str(e)}")
            raise
        finally:
            await self.pool.release(channel)

    async def close(self):
        await self.pool.close()
