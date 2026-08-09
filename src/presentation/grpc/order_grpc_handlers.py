from src.presentation.mappers.order_mapper import OrderResponseMapper
from src.application.use_cases.order.interfaces.get_order_usecase_interface import IGetOrderUseCase
from src.application.use_cases.order.interfaces.get_orders_usecase_interface import IGetOrdersUseCase
from src.application.use_cases.order.interfaces.get_revenue_status_usecase_interface import IGetRevenueStatsUseCase
from src.application.use_cases.order.interfaces.place_order_usecase_interface import IPlaceOrderUseCase
from src.application.use_cases.order.interfaces.restore_order_usecase_interface import IRestoreOrderUseCase
from src.infrastructure.grpc.generated.order_service_pb2 import RevenueStatsData
from grpc import  aio
from src.application.dtos.restore_order_dto import RestoreOrderDto
from src.presentation.grpc.helpers.exception_hanlders import  handle_grpc_exception
from src.shared.utils.get_metadata import get_metadata_value
from src.domain.exceptions.exceptions import DomainException
from src.application.dtos.get_order_dto import GetOrderDto
from src.application.dtos.get_orders_by_user_dto import GetOrdersByUserDto
from src.application.interfaces.logging_interface import ILoggingService
from src.application.dtos.order_create_dto import OrderCreateDto
from src.infrastructure.grpc.auth_guard import AuthGuard
from src.infrastructure.grpc.generated.order_service_pb2 import (
    GetOrdersRequest,
    GetRevenueStatsResponse,
    OrderResponse,
    OrderStatus,
    OrderStatusResponse,
    OrderSuccess,
    OrdersResponse,
    OrdersSuccess,
    RevenueStats,
)
from src.infrastructure.grpc.generated.order_service_pb2_grpc import OrderServiceServicer

class OrderServiceHandler(OrderServiceServicer):
    def __init__(self,
                 place_order_use_case: IPlaceOrderUseCase,
                 get_order_use_case: IGetOrderUseCase,
                 get_revenue_stats_use_case: IGetRevenueStatsUseCase,
                 restore_order_use_case: IRestoreOrderUseCase,
                 get_orders_use_case: IGetOrdersUseCase,
                #  book_session_use_case: BookSessionUseCase,
                 logger: ILoggingService
                 ):
        self.place_order_use_case = place_order_use_case
        self.get_order_use_case = get_order_use_case
        self.get_order_use_case = get_order_use_case
        self.get_revenue_stats_use_case = get_revenue_stats_use_case
        self.restore_order_use_case = restore_order_use_case
        self.get_orders_use_case = get_orders_use_case
        # self.book_session_use_case = book_session_use_case
        self.logger = logger.get_logger("OrderServiceHandler")

   

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
                success=OrderSuccess(order=OrderResponseMapper.to_grpc_response(result))
            )
        except Exception as e:
            return await handle_grpc_exception(
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
                success=OrderSuccess(order=OrderResponseMapper.to_grpc_response(result))

            )

        except Exception as e:
            self.logger.error(f"Failed to get order: {str(e)}")
            return await handle_grpc_exception(
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
                success=OrderSuccess(order=OrderResponseMapper.to_grpc_response(result))

            )

        except Exception as e:
            self.logger.error(f"Failed to restore order: {str(e)}")
            return await handle_grpc_exception(
                e,
                context,
                OrderResponse,
                operation="restore order",
                default_message="Failed to restore order  order",
                logger=self.logger
            )

    async def GetRevenueStats(self, request, context: aio.ServicerContext):
        self.logger.info(
            f"Received GetRevenueStats request for year {request.year}")
        try:
            stats = await self.get_revenue_stats_use_case.execute(request.year)
            self.logger.info(f"Fetched revenue stats for year {request.year}: {stats}")
            revenue_stats = [RevenueStats(
                        month=stat.get("month", 0),
                        revenue=stat.get("revenue", 0)  
                    ) for stat in stats]
            self.logger.info("Mapped revenue_status " + str(revenue_stats))
            return GetRevenueStatsResponse(
                success=RevenueStatsData(
                    revenue_stats=revenue_stats
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to get revenue stats: {str(e)}")
            return await handle_grpc_exception(
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
            return await handle_grpc_exception(
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
                    orders=[OrderResponseMapper.to_grpc_response(order)
                            for order in result["orders"]],
                    total=result["total"]),


            )

        except Exception as e:
            self.logger.error(f"Failed to get orders: {str(e)}")
            return await handle_grpc_exception(
                e,
                context,
                OrdersResponse,
                operation="place order",
                default_message="Failed to get order status",
                logger=self.logger
            )

    