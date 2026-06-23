from src.application.dtos.restore_order_dto import RestoreOrderDto
from src.infrastructure.database.database import get_db
from src.application.dtos.get_order_dto import GetOrderDto
from src.domain.exceptions.exceptions import OrderNotFoundException
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.domain.repositories.order_repository import IOrderRepository
from src.application.dtos.order_dto import OrderDto
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from tenacity import retry, stop_after_attempt, wait_exponential


class RestoreOrderUseCase:
    def __init__(
        self,
        order_repository: IOrderRepository,
        kafka_producer: IKafkaProducer,
        redis: IRedisService,
        logging_service: ILoggingService,
        metrics_service: IMetricsService,
    ):
        self._order_repository = order_repository
        self._kafka_producer = kafka_producer
        self._cache = redis
        self._logger = logging_service.get_logger("RestoreOrderUseCase")
        self._metrics = metrics_service

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def execute(self, dto: RestoreOrderDto) -> OrderDto:
        self._logger.info(
            f"Executing RestoreOrderUseCase order id {dto.order_id}")

        # Create order
        async with get_db() as session:
            order = await self._order_repository.find_by_id(dto.order_id, session)
            if not order:
                self._logger.error(f"Order not found with Id {dto.order_id}")
                raise OrderNotFoundException(f"Order not found with Id {dto.order_id}")

            if order.user_id != dto.user_id:
                self._logger.warning(
                    f"User ID mismatch: order.user_id={order.user_id}, dto.user_id={dto.user_id}"
                )
                raise OrderNotFoundException("Order does not belong to the requesting user.")

            order.reset()
            await self._order_repository.save(order, session)

        # Invalidate cache for related user orders
        self._logger.debug(
            f"Successfully restored  order for  order id {dto.order_id} ")

        return OrderDto.from_domain(order)
