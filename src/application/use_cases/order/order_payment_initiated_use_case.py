from  datetime import datetime, timezone
from uuid import uuid4
from src.domain.events.order_payment_initiate_event import OrderPaymentInitiatedEventDto
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.redis_interface import IRedisService
from src.domain.entities.payment_details import PaymentDetails, PaymentStatus
from src.domain.repositories.order_repository import IOrderRepository
from src.infrastructure.database.database import get_db
from src.domain.exceptions.exceptions import OrderNotFoundException
from tenacity import retry, stop_after_attempt, wait_exponential


class OrderPaymentInitiatedUseCase:
    def __init__(self, order_repository: IOrderRepository,
                 kafka_producer: IKafkaProducer,
                 redis: IRedisService,
                 logging_service: ILoggingService,
                 metrics_service: IMetricsService,
                 ):
        self._order_repository = order_repository
        self._kafka_producer = kafka_producer
        self._cache = redis
        self._logger = logging_service.get_logger(
            "OrderPaymentInitiatedUseCase")
        self._metrics = metrics_service

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def execute(self, dto: OrderPaymentInitiatedEventDto):
        payload = dto.payload
        self._logger.info(f"Initiating payment for order {payload.order_id}")

        async with get_db() as session:
            order = await self._order_repository.find_by_id(payload.order_id, session)
            if not order:
                raise OrderNotFoundException(
                    f"Order not found: {payload.order_id}")

            if order.payment_details is None:
                order.payment_details = PaymentDetails(
                    id=str(uuid4()),
                    payment_id=payload.payment_id,
                    provider=payload.provider,
                    provider_order_id=payload.provider_order_id,
                    payment_status="pending",
                    updated_at=datetime.fromtimestamp(int(dto.timestamp) / 1000, tz=timezone.utc),
                )
                
            order.mark_processing() 

            await self._order_repository.save(order, session)

        self._logger.debug(f"Payment initiated for order {payload.order_id}")
        return
