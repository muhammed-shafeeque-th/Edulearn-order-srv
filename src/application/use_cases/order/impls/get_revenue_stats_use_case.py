from typing import List
from src.application.use_cases.order.interfaces.get_revenue_status_usecase_interface import IGetRevenueStatsUseCase
from src.infrastructure.database.database import get_db
from src.domain.exceptions.exceptions import OrderNotFoundException
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.domain.repositories.order_repository import IOrderRepository, RevenueRange, RevenueStats
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from tenacity import retry, stop_after_attempt, wait_exponential


class GetRevenueStatsUseCase(IGetRevenueStatsUseCase):
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
        self._logger = logging_service.get_logger("GetRevenueStatsUseCase")
        self._metrics = metrics_service

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def execute(self, year: int) -> List[RevenueStats]:
       
        
        self._logger.info(
            f"Executing GetRevenueStatsUseCase for year '{year}'"
        )

        async with get_db() as session:
            stats = await self._order_repository.get_revenue_stats(year, session)

        if stats is None or not isinstance(stats, list):
            self._logger.error(f"No revenue stats found for year '{year}'")
            raise OrderNotFoundException(f"Revenue statistics not found for year: {year}")

        self._logger.debug(
            f"Successfully fetched revenue stats for year '{year}': {stats}"
        )
        
        return stats
