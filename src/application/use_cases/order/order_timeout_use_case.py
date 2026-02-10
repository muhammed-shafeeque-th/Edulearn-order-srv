from src.domain.events.order_failed_event import OrderFailedEvent, OrderFailedEventType
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.redis_interface import IRedisService
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.events.order_payment_timeout_event import OrderPaymentTimeoutEventDto
from src.domain.entities.payment_details import PaymentDetails, PaymentStatus
from src.shared.events.topics import EVENT_TOPICS
from src.infrastructure.database.database import get_db
from src.domain.exceptions.exceptions import OrderNotFoundException
from tenacity import retry, stop_after_attempt, wait_exponential
from datetime import datetime, timezone
from uuid import uuid4 as uuidV4


class HandleOrderTimeoutUseCase:
    def __init__(self,  order_repository: IOrderRepository,
                 kafka_producer: IKafkaProducer[OrderFailedEventType],
                 redis: IRedisService,
                 logging_service: ILoggingService,
                 metrics_service: IMetricsService):
        self.order_repository = order_repository
        self.kafka_producer = kafka_producer
        self.redis = redis
        self.logger = logging_service.get_logger(
            "HandleOrderTimeoutUseCase")
        self.metrics = metrics_service

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def execute(self, dto: OrderPaymentTimeoutEventDto):
        payload = dto.payload
        
        self.logger.info(f"Processing HandleOrderTimeoutUseCase for order {payload.order_id}")

        async with get_db() as session:
            order = await self.order_repository.find_by_id(payload.order_id, session)
            if not order:
                raise OrderNotFoundException(
                    f"Order not found: {payload.order_id}")

            if not order.payment_details:
                payment_details = PaymentDetails(
                    id=str(uuidV4()),
                    payment_id=payload.payment_id,
                    provider=payload.provider,
                    provider_order_id=payload.provider_order_id,
                    updated_at=datetime.fromtimestamp(
                        int(dto.timestamp) / 1000, tz=timezone.utc),
                    payment_status="expired",
                )
                order.set_payment_details(payment_details)
            else:
                order.payment_details.mark_expired()

            order.mark_expired()
            await self.order_repository.save(order, session)

        await self.kafka_producer.publish_event(
            EVENT_TOPICS.ORDER_COURSE_FAILED.value,
            event=OrderFailedEvent(
                orderId=order.id,
                userId=order.user_id,
                items=[{"courseId": i.course_id, "price": i.price}
                       for i in order.items],
                amount=order.amount.amount,
                currency=order.amount.currency,
            ).to_dict(),
            schema=None,
        )

        self.logger.warning(f"Order {payload.order_id} marked as EXPIRED")
        return
