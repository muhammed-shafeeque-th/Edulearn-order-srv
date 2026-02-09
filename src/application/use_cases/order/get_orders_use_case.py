from typing import TypedDict
from src.application.dtos.get_orders_by_user_dto import GetOrdersByUserDto
from src.infrastructure.database.database import get_db
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.domain.repositories.order_repository import IOrderRepository
from src.application.dtos.order_dto import OrderDto
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from tenacity import retry, stop_after_attempt, wait_exponential

class OrdersUseCaseResponse(TypedDict):
    orders: list[OrderDto]
    total: int

class GetOrdersUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        kafka_producer: IKafkaProducer,
        redis: IRedisService,
        logging_service: ILoggingService,
        metrics_service: IMetricsService,
    ):
        self.order_repository = order_repository
        self.kafka_producer = kafka_producer
        self.redis = redis
        self.logging_service = logging_service
        self.logger = logging_service.get_logger("GetOrdersUseCase")
        self.metrics = metrics_service

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def execute(self, dto: GetOrdersByUserDto) -> OrdersUseCaseResponse:
        self.logger.info(
            f"Executing GetOrdersUseCase for user {dto.user_id}")

        async with get_db() as session:
            orders, total = await self.order_repository.find_by_user_id(dto.user_id, session, sort_order=dto.sort_order, page=dto.page, page_size=dto.page_size, status=dto.status)

        self.logger.debug(
            f"Successfully fetched {len(orders)} orders for  user {dto.user_id} ")

        return {
            "orders": [OrderDto.from_domain(order) for order in orders],
            "total": total
        }
