from typing import Callable

from src.presentation.grpc.order_grpc_handlers import OrderServiceHandler
import asyncio
from grpc import  aio
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.tracing_interface import ITracingService
from src.infrastructure.grpc.auth_guard import AuthGuard
from src.infrastructure.grpc.generated.order_service_pb2_grpc import  add_OrderServiceServicer_to_server
from src.infrastructure.grpc.interceptors.server_interceptor import (
    ServerLoggingInterceptor,
    ServerMetricsInterceptor,
    ServerTracingInterceptor,
)
from src.infrastructure.config.settings import settings


class OrderGrpcServer:
    def __init__(self,
                    grpc_handlers: OrderServiceHandler,
                    auth_guard: AuthGuard,
                    logger_service: ILoggingService,
                    metrics: IMetricsService,
                    tracer: ITracingService,
                 ):

        # self.book_session_use_case = book_session_use_case
        self.logger = logger_service.get_logger("OrderServiceImpl")
        self.logger_service = logger_service
        self.handlers = grpc_handlers
        self.metrics = metrics
        self.tracer = tracer

   

    async def start_server(self):
        server = aio.server(
            interceptors=[
                ServerLoggingInterceptor(self.logger_service),
                ServerMetricsInterceptor(logger=self.logger_service, metrics=self.metrics),
                ServerTracingInterceptor(tracer=self.tracer),
                # ServerAuthInterceptor(auth_guard, logger_service),
            ]
        )
        add_OrderServiceServicer_to_server(
            self.handlers,server
        )
        logger = self.logger_service.get_logger("start_grpc_server")
        server.add_insecure_port(f'[::]:{settings.GRPC_PORT}')
        logger.info(f"Starting gRPC server on port {settings.GRPC_PORT}")
        await server.start()
        try:
            await server.wait_for_termination()
        except asyncio.CancelledError:
            logger.info(
                "gRPC server cancellation received; initiating graceful shutdown")
            raise
        finally:
            # Ensure server is stopped before the event loop closes to avoid warnings
            await server.stop(grace=1)


    
    
            


