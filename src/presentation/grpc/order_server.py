from typing import Any
import asyncio
from grpc import  aio
from tenacity import RetryError
from src.application.use_cases.order.get_revenue_stats_use_case import GetRevenueStatsUseCase
from src.application.dtos.restore_order_dto import RestoreOrderDto
from src.presentation.grpc.helpers.exception_hanlders import create_error_response, create_grpc_service_error, handle_grpc_exception
from src.shared.utils.get_metadata import get_metadata_value
from src.domain.exceptions.exceptions import DomainException
from src.application.dtos.get_order_dto import GetOrderDto
from src.application.dtos.get_orders_by_user_dto import GetOrdersByUserDto
from src.application.use_cases.order.get_order_use_case import GetOrderUseCase
from src.application.use_cases.order.get_orders_use_case import GetOrdersUseCase
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.tracing_interface import ITracingService
from src.infrastructure.observability.logging_service import LoggingService
from src.application.dtos.order_create_dto import OrderCreateDto
from pydantic import ValidationError
from src.application.dtos.session_booking_create_dto import SessionBookingCreateDTO
from src.application.use_cases.session_booking.session_booking_use_case import BookSessionUseCase
from src.infrastructure.grpc.auth_guard import AuthGuard
from src.infrastructure.grpc.generated.order_service_pb2 import (
    GetOrdersRequest,
    GetRevenueStatsResponse,
    OrderResponse,
    OrderStatus,
    OrderStatusResponse,
    OrderSuccess,
    OrdersResponse,
    BookSessionResponse,
    OrdersSuccess,
    BookSessionSuccess,
    RevenueStats,
)
from src.infrastructure.grpc.generated.order_service_pb2_grpc import OrderServiceServicer, add_OrderServiceServicer_to_server
from src.application.use_cases.order.place_order_use_case import PlaceOrderUseCase
from src.application.use_cases.order.restore_order_use_case import RestoreOrderUseCase
from src.infrastructure.grpc.interceptors.server_interceptor import (
    ServerLoggingInterceptor,
    ServerMetricsInterceptor,
    ServerTracingInterceptor,
)
from src.infrastructure.config.settings import settings


class OrderServiceImpl(OrderServiceServicer):
    def __init__(self,
                 place_order_use_case: PlaceOrderUseCase,
                 get_order_use_case: GetOrderUseCase,
                 get_revenue_stats_use_case: GetRevenueStatsUseCase,
                 restore_order_use_case: RestoreOrderUseCase,
                 get_orders_use_case: GetOrdersUseCase,
                 book_session_use_case: BookSessionUseCase,
                 logger: ILoggingService
                 ):
        self.place_order_use_case = place_order_use_case
        self.get_order_use_case = get_order_use_case
        self.get_order_use_case = get_order_use_case
        self.get_revenue_stats_use_case = get_revenue_stats_use_case
        self.restore_order_use_case = restore_order_use_case
        self.get_orders_use_case = get_orders_use_case
        self.book_session_use_case = book_session_use_case
        self.logger = logger.get_logger("OrderServiceImpl")

   

    async def PlaceOrder(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received PlaceOrder request for user {request.user_id}")
        try:
            self.logger.info("place order request " + str(request))
            # The proto defines optional coupon as `coupon_code`; map it to DTO's coupon_id
            coupon_code = request.coupon_code if hasattr(
                request, 'coupon_code') and request.coupon_code else None
            order_dto = OrderCreateDto(
                user_id=request.user_id,
                coupon_code=coupon_code,
                course_ids=list(request.course_ids),
            )
            auth_token = get_metadata_value(
                context, "authorization", strip_prefix="Bearer ")
            idempotency_key = get_metadata_value(
                context, "idempotency-key", cast=lambda x: str(x))

            result = await self.place_order_use_case.execute(order_dto, idempotency_key)
            self.logger.info(f"Order {result.id} placed successfully")
            return OrderResponse(
                success=OrderSuccess(order=result.to_response_data())
            )
        except Exception as e:
            return handle_grpc_exception(
                e,
                context,
                OrderResponse,
                operation="place order",
                default_message="Failed to place order",
                logger=self.logger
            )

    async def GetOrderById(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received GetOrderById request for user {request.order_id}")
        try:
            order_dto = GetOrderDto(
                order_id=request.order_id)
            result = await self.get_order_use_case.execute(order_dto)
            self.logger.info(f"fetched order with id {request.order_id}")
            return OrderResponse(
                success=OrderSuccess(order=result.to_response_data())

            )

        except Exception as e:
            self.logger.error(f"Failed to get order: {str(e)}")
            return handle_grpc_exception(
                e,
                context,
                OrderResponse,
                operation="place order",
                default_message="Failed to get order  order",
                logger=self.logger
            )
    async def RestoreOrder(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received RestoreOrder request for order {request.order_id}")
        try:
            order_dto = RestoreOrderDto(
                order_id=request.order_id, user_id=request.user_id)
            result = await self.restore_order_use_case.execute(order_dto)
            self.logger.info(f"restored order with id {request.order_id}")
            return OrderResponse(
                success=OrderSuccess(order=result.to_response_data())

            )

        except Exception as e:
            self.logger.error(f"Failed to restore order: {str(e)}")
            return handle_grpc_exception(
                e,
                context,
                OrderResponse,
                operation="restore order",
                default_message="Failed to restore order  order",
                logger=self.logger
            )

    async def GetRevenueStats(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received GetRevenueStats request for range {request.range}")
        try:
            stats = await self.get_revenue_stats_use_case.execute(request.range)
            self.logger.info(f"Fetched revenue stats for range {request.range}: {stats}")
            return GetRevenueStatsResponse(
                success=RevenueStats(
                    revenue_this_month=stats.get("revenue_this_month", 0),
                    revenue_last_month=stats.get("revenue_last_month", 0)
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to get revenue stats: {str(e)}")
            return handle_grpc_exception(
                exc=e,
                ctx=context,
                response_model=GetRevenueStatsResponse,
                operation="get revenue stats",
                default_message="Failed to get revenue stats",
                logger=self.logger
            )
    async def GetOrderStatus(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received GetOrderStatus request for user {request.order_id}")
        try:
            order_dto = GetOrderDto(
                order_id=request.order_id)
            result = await self.get_order_use_case.execute(order_dto)
            self.logger.info(f"fetched status with id {request.order_id}")
            return OrderStatusResponse(
                success=OrderStatus(order_id=result.id,
                                    status=result.status.value)

            )

        except Exception as e:
            self.logger.error(f"Failed to get order status: {str(e)}")
            return handle_grpc_exception(
                exc=e,
                ctx=context,
                response_model=OrderResponse,
                operation="place order",
                default_message="Failed to get order status",
                logger=self.logger
            )

    async def GetOrders(self, request: GetOrdersRequest, context: aio.ServicerContext):
        self.logger.info(
            f"Received GetOrders request for user {request.user_id}")
        try:
            
            order_dto = GetOrdersByUserDto.from_proto(
                user_id=request.user_id, proto_obj=request.params)
            result = await self.get_orders_use_case.execute(order_dto)
            self.logger.info(f"Fetched orders {request.user_id}")
            return OrdersResponse(
                success=OrdersSuccess(
                    orders=[order.to_response_data()
                            for order in result["orders"]],
                    total=result["total"]),


            )

        except Exception as e:
            self.logger.error(f"Failed to get orders: {str(e)}")
            return handle_grpc_exception(
                e,
                context,
                OrdersResponse,
                operation="place order",
                default_message="Failed to get order status",
                logger=self.logger
            )

    async def BookSession(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received BookSession request for user {request.user_id}")
        try:
            booking_dto = SessionBookingCreateDTO(
                user_id=request.user_id, session_id=request.session_id)
            result = await self.book_session_use_case.execute(booking_dto)
            self.logger.info(
                f"Session booking {result.id} created successfully")
            return BookSessionResponse(
                success=BookSessionSuccess(
                    id=result.id,
                    user_id=result.user_id,
                    session_id=result.session_id,
                    amount=result.amount,
                    currency=result.currency,
                    status=result.status,
                    created_at=result.created_at.isoformat(),
                    updated_at=result.updated_at.isoformat(),
                )
            )
        except DomainException as e:
            return OrderResponse(
                error=create_error_response(
                    code=type(e).__name__,
                    message=str(e),
                    details=[{"field": "request", "message": str(e)}]
                )
            )
        except ValidationError as ve:
            details = []
            for err in ve.errors():
                field_path = ".".join(str(p) for p in err.get("loc", []))
                details.append({
                    "field": field_path or "request",
                    "message": err.get("msg", "Invalid value"),
                })
            self.logger.error(f"Validation error in PlaceOrder: {ve}")
            return OrderResponse(
                error=create_error_response(
                    code="INVALID_ARGUMENT",
                    message="Invalid request data",
                    details=details,
                )
            )

        except Exception as e:
            self.logger.error(f"Failed to book session: {str(e)}")
            return create_grpc_service_error(
                    ctx=context,
                    code="INTERNAL",
                    message="Failed to book session",
                    details=[{"field": "service", "message": str(e)}]
            )

    
    
            


async def start_grpc_server(
    place_order_use_case: PlaceOrderUseCase,
    book_session_use_case: BookSessionUseCase,
    get_order_use_case: GetOrderUseCase,
    get_revenue_stats_use_case: GetRevenueStatsUseCase,
    restore_order_use_case: RestoreOrderUseCase,
    get_orders_use_case: GetOrdersUseCase,
    auth_guard: AuthGuard,
    logger_service: ILoggingService,
    metrics: IMetricsService,
    tracer: ITracingService,
):
    server = aio.server(
        interceptors=[
            ServerLoggingInterceptor(logger_service),
            ServerMetricsInterceptor(logger=logger_service, metrics=metrics),
            ServerTracingInterceptor(),
            # ServerAuthInterceptor(auth_guard, logger_service),
        ]
    )
    add_OrderServiceServicer_to_server(
        OrderServiceImpl(place_order_use_case,
                         get_order_use_case,
                         get_revenue_stats_use_case,
                         restore_order_use_case,
                         get_orders_use_case,
                         book_session_use_case, logger_service), server
    )
    logger = logger_service.get_logger("start_grpc_server")
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
