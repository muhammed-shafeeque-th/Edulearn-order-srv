from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.redis_interface import IRedisService
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.events.order_expired_event import OrderExpiredEvent
from src.shared.events.topics import EVENT_TOPICS
from src.infrastructure.database.database import get_db
from src.domain.exceptions.exceptions import OrderNotFoundException
from tenacity import retry, stop_after_attempt, wait_exponential

class ExpireOrderUseCase:
    def __init__(self,  order_repository: IOrderRepository,
                 kafka_producer: IKafkaProducer,
                 redis: IRedisService,
                 logging_service: ILoggingService,
                 metrics_service: IMetricsService):
        self._order_repository = order_repository
        self._kafka_producer = kafka_producer
        self._cache = redis
        self._logger = logging_service.get_logger("ExpireOrderUseCase")
        self._metrics = metrics_service

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def execute(self, order_id: str):
        self._logger.info(f"Processing ExpireOrderUseCase for order {order_id}")

        async with get_db() as session:
            order = await self._order_repository.find_by_id(order_id, session)
            if not order:
                raise OrderNotFoundException(f"Order not found: {order_id}")

            # If it's already in a terminal state, skip
            if order.status.value in ["succeeded", "failed", "cancelled", "refunded", "expired"]:
                self._logger.info(f"Order {order_id} is already in terminal state {order.status.value}, skipping expiry")
                return

            if order.payment_details:
                order.payment_details.mark_expired()

            order.mark_expired()
            await self._order_repository.save(order, session)
            await session.commit()

        await self._kafka_producer.publish_event(
            EVENT_TOPICS.ORDER_COURSE_EXPIRED.value,
            event=OrderExpiredEvent(
                orderId=order.id,
                userId=order.userId if hasattr(order, 'userId') else order.user_id,
                items=[{"courseId": i.course_id, "price": i.price} for i in order.items],
                amount=order.amount.amount,
                currency=order.amount.currency,
            ).to_dict(),
            schema=None,
        )

        self._logger.info(f"Order {order_id} successfully marked as EXPIRED and event published")
        return
