import json
from aiokafka import AIOKafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from src.application.use_cases.order.order_timeout_use_case import HandleOrderTimeoutUseCase
from src.domain.events.order_payment_timeout_event import OrderPaymentTimeoutEventDto
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.redis_interface import IRedisService
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.domain.exceptions.exceptions import OrderNotFoundException
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.repositories.session_booking_repository import ISessionBookingRepository
from src.infrastructure.config.settings import settings
from src.shared.events.topics import EVENT_TOPICS

from src.application.use_cases.order.order_payment_initiated_use_case import OrderPaymentInitiatedUseCase
from src.application.use_cases.order.order_success_use_case import OrderSuccessUseCase
from src.application.use_cases.order.order_failed_use_case import OrderFailedUseCase

from src.domain.events.order_payment_initiate_event import OrderPaymentInitiatedEventDto
from src.domain.events.order_payment_failure_event import OrderPaymentFailureEventDto
from src.domain.events.order_payment_success_event import OrderPaymentSuccessEventDto
from tenacity import RetryError
from pydantic import ValidationError

from typing import Any


class KafkaConsumer:
    DLQ_TOPIC = "order-service.events.dlq"
    MAX_WORKERS = 10

    def __init__(
        self,
        order_repository: IOrderRepository,
        session_booking_repository: ISessionBookingRepository,
        payment_initiated_handler: OrderPaymentInitiatedUseCase,
        order_success_handler:  OrderSuccessUseCase,
        order_failed_handler: OrderFailedUseCase,
        order_timeout_handler: HandleOrderTimeoutUseCase,
        kafka_producer: IKafkaProducer,
        redis: IRedisService,
        metrics_service: IMetricsService,
        logging_service: ILoggingService,
    ):

        payment_topics = [
            EVENT_TOPICS.PAYMENT_ORDER_INITIATED.value,
            EVENT_TOPICS.PAYMENT_ORDER_SUCCEEDED.value,
            EVENT_TOPICS.PAYMENT_ORDER_FAILED.value,
            EVENT_TOPICS.PAYMENT_ORDER_TIMEOUT.value,
        ]

        self.consumer = AIOKafkaConsumer(
            *payment_topics,
            bootstrap_servers=settings.KAFKA_BROKER,
            group_id=settings.KAFKA_CONSUMER_GROUP or "order-service-group",
            auto_offset_reset="latest",
            enable_auto_commit=False,
            max_poll_records=settings.KAFKA_CONSUMER_MAX_POLL_RECORDS,
        )

        self.order_repository = order_repository
        self.session_booking_repository = session_booking_repository

        self.payment_initiated_handler = payment_initiated_handler
        self.order_success_handler = order_success_handler
        self.order_timeout_handler = order_timeout_handler
        self.order_failed_handler = order_failed_handler

        self.kafka_producer = kafka_producer
        self.redis = redis
        self.metrics_service = metrics_service
        self.logger = logging_service.get_logger("KafkaConsumer")

        self.dlq_topic = self.DLQ_TOPIC

        self.executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

    async def start(self):
        await self.consumer.start()
        self.logger.info(
            "Kafka Consumer started and listening for order events...")

        try:
            async for msg in self.consumer:
                try:
                    await self.handle_message(msg)
                except Exception as msg_exc:
                    # Don't let a single message crash the loop
                    self.logger.error(
                        f"Error within message handling loop: {msg_exc}")
                await self.consumer.commit()
        except Exception as e:
            self.logger.error(f"Consumer crashed: {str(e)}")
        finally:
            await self.consumer.stop()
            self.executor.shutdown(wait=False)  # Don't block on threads

    async def handle_message(self, msg: Any) -> None:
        """Process a single Kafka message with error handling and send to DLQ on failure."""
        try:
            payload = json.loads(msg.value.decode("utf-8"))
            topic = msg.topic
            self.logger.info(
                f"Received event from topic: {topic} with payload: {payload}")
            await self.route_event(topic, payload)
        except json.JSONDecodeError as jde:
            self.logger.error(
                f"Invalid JSON in message from topic {getattr(msg, 'topic', 'unknown')}: {jde}"
            )
            await self.send_to_dlq(msg, error="JSONDecodeError")
        except Exception as e:
            self.logger.error(
                f"Error processing message from {getattr(msg, 'topic', 'unknown')}: {e}")
            await self.send_to_dlq(msg, error=str(e))

    async def route_event(self, topic: str, event: dict) -> None:
        """Routes event to appropriate handler based on topic."""
        try:
            if topic == EVENT_TOPICS.PAYMENT_ORDER_INITIATED.value:
                dto = OrderPaymentInitiatedEventDto.from_payload(
                    event=event,
                )
                await self.payment_initiated_handler.execute(dto)

            elif topic == EVENT_TOPICS.PAYMENT_ORDER_SUCCEEDED.value:
                dto = OrderPaymentSuccessEventDto.from_payload(
                    event=event,
                )
                await self.order_success_handler.execute(dto)

            elif topic == EVENT_TOPICS.PAYMENT_ORDER_FAILED.value:
                dto = OrderPaymentFailureEventDto.from_payload(

                    event=event,
                )
                await self.order_failed_handler.execute(dto)
            elif topic == EVENT_TOPICS.PAYMENT_ORDER_TIMEOUT.value:
                dto = OrderPaymentTimeoutEventDto.from_payload(
                    event=event,
                )
                await self.order_timeout_handler.execute(dto)

            else:
                self.logger.warning(f"Unknown topic received: {topic}")

        except ValidationError as ve:
            self.logger.error(
                f"Pydantic ValidationError for topic {topic}: {ve}")
            await self.send_to_dlq_from_payload(topic, event, error=f"PydanticValidationError: {ve}")
        except OrderNotFoundException as e:
            self.logger.error(f"Order not found: {str(e)}")
            await self.send_to_dlq_from_payload(topic, event, error=str(e))
        except RetryError as retry_err:
            last_exc = getattr(retry_err, 'last_attempt', None)
            error_msg = None
            if last_exc and hasattr(last_exc, 'exception') and last_exc.exception():
                err = last_exc.exception()
                error_msg = str(err)
                self.logger.error(
                    f"RetryError while processing event for {topic}: {str(retry_err)} | Real error: {error_msg}"
                )
                error_detail = f"RetryError: {error_msg}"
            else:
                self.logger.error(
                    f"RetryError while processing event for {topic}: {str(retry_err)}"
                )
                error_detail = f"RetryError: {str(retry_err)}"

            await self.send_to_dlq_from_payload(topic, event, error=error_detail)

        except Exception as e:
            self.logger.error(f"Failed to process event for {topic}: {str(e)}")
            await self.send_to_dlq_from_payload(topic, event, error=str(e))

    async def send_to_dlq(self, msg: Any, error: str) -> None:
        """Send failed message to Dead Letter Queue."""
        try:
            message_value = msg.value.decode(
                "utf-8", errors="ignore") if hasattr(msg, "value") else str(msg)
            dlq_event = {
                "eventType": "DLQEvent",
                "originalTopic": getattr(msg, "topic", ""),
                "originalMessage": message_value,
                "error": error,
                "timestamp": datetime.utcnow().isoformat(),
            }
            await self.kafka_producer.publish_event(self.dlq_topic, event=dlq_event, schema=None)
            self.logger.warning(f"Sent message to DLQ topic {self.dlq_topic}")
        except Exception as e:
            self.logger.error(f"Failed to publish to DLQ: {e}")

    async def send_to_dlq_from_payload(self, topic: str, payload: dict, error: str):
        """Send failed payload (non-message object) to DLQ"""
        dlq_event = {
            "eventType": "DLQEvent",
            "originalTopic": topic,
            "originalMessage": json.dumps(payload),
            "error": error,
            "timestamp": datetime.utcnow().isoformat(),
        }
        await self.kafka_producer.publish_event(self.dlq_topic, event=dlq_event, schema=None)
        self.logger.warning(f"Sent payload to DLQ topic {self.dlq_topic}")
