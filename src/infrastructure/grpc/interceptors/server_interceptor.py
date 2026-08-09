from typing import Awaitable, Callable
from grpc import HandlerCallDetails, RpcMethodHandler, aio
import grpc
from opentelemetry import propagate, trace
from opentelemetry.trace import SpanKind
import time
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.tracing_interface import ITracingService
from src.infrastructure.config import settings
from src.infrastructure.grpc.auth_guard import AuthGuard


class ServerLoggingInterceptor(aio.ServerInterceptor):
    def __init__(self, logger: ILoggingService) -> None:
        self.logger = logger.get_logger("ServerLoggingInterceptor")

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        method = handler_call_details.method
        self.logger.info(f"Received gRPC request: {method}")
        return await continuation(handler_call_details)


class ServerMetricsInterceptor(aio.ServerInterceptor):
    def __init__(self, metrics: IMetricsService, logger: ILoggingService) -> None:
        self.logger = logger.get_logger("ServerMetricsInterceptor")
        self.metrics = metrics

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        method = handler_call_details.method
        start_time = time.time()
        status = "unknown"

        try:
            response = await continuation(handler_call_details)
            status = "success"
        except Exception as e:
            status = "failed"
            raise
        finally:
            latency = time.time() - start_time
            self.metrics.request_counter(
                method=method, endpoint=method, status=status)
            self.metrics.request_latency(
                method=method, endpoint=method, latency=latency)
            self.logger.debug(
                f"gRPC method ${method} completed wit status ${status} in ${latency//1000}s"
            )
        return response


class ServerTracingInterceptor(aio.ServerInterceptor):
    def __init__(self, tracer: ITracingService,) -> None:
        self.tracer = tracer.get_tracer()

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        method = handler_call_details.method
        metadata = dict(handler_call_details.invocation_metadata)

        # Extract span context from metadata
        span_context = propagate.extract(metadata)
        with self.tracer.start_as_current_span(
            method, context=span_context, kind=SpanKind.SERVER
        ) as span:
            span.set_attribute("grpc.method", method)
            return await continuation(handler_call_details)


class ServerAuthInterceptor(aio.ServerInterceptor):
    def __init__(self, auth_guard: AuthGuard, logger: ILoggingService) -> None:
        self.auth_guard = auth_guard
        self.logger = logger.get_logger("ServerAuthInterceptor")

    async def intercept_service(
        self,
        continuation: Callable[[HandlerCallDetails], Awaitable[RpcMethodHandler]],
        handler_call_details: HandlerCallDetails,
    ) -> RpcMethodHandler:
        metadata = dict(handler_call_details.invocation_metadata)
        token = str(metadata.get("authorization", "")).replace("Bearer ", "")

        if not token:
            self.logger.error("Authorization token missing")
            raise grpc.RpcError(
                grpc.StatusCode.UNAUTHENTICATED, "Authorization token missing"
            )

        try:
            user_info = await self.auth_guard.validate_token(token)
            await self.auth_guard.authorize(user_info, "STUDENT")
        except Exception as e:
            self.logger.error(f"Auth failed: {str(e)}")
            raise grpc.RpcError(grpc.StatusCode.UNAUTHENTICATED, str(e))

        return await continuation(handler_call_details)
