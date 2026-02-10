from src.infrastructure.database.database import get_db
from src.application.dtos.get_order_dto import GetOrderDto
from src.domain.exceptions.exceptions import OrderNotFoundException
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.domain.repositories.order_repository import IOrderRepository, RevenueRange, RevenueStats
from src.application.dtos.order_dto import OrderDto
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from tenacity import retry, stop_after_attempt, wait_exponential


class GetRevenueStatsUseCase:
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
        self.logger = logging_service.get_logger("GetRevenueStatsUseCase")
        self.metrics = metrics_service

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def execute(self, range: RevenueRange) -> RevenueStats:
        """
        Executes the use case to retrieve revenue statistics for a given range.
        
        Args:
            range (RevenueRange): The range for which to get revenue statistics ("thisMonth", "lastMonth").
        
        Returns:
            dict: Revenue statistics for the specified period.
        """
        self.logger.info(
            f"Executing GetRevenueStatsUseCase for range '{range}'"
        )

        async with get_db() as session:
            stats = await self.order_repository.get_revenue_stats(range, session)

        if stats is None or not isinstance(stats, dict):
            self.logger.error(f"No revenue stats found for range '{range}'")
            raise OrderNotFoundException(f"Revenue statistics not found for range: {range}")

        self.logger.debug(
            f"Successfully fetched revenue stats for range '{range}': {stats}"
        )

        return stats
