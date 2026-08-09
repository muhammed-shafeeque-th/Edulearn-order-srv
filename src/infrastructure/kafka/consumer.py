import json
from aiokafka import AIOKafkaConsumer
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from src.presentation.kafka.kafka_handlers import KafkaEventHandlers
from src.infrastructure.kafka.handler_registry import UnknownTopicError
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.domain.exceptions.exceptions import OrderNotFoundException
from src.infrastructure.config.settings import settings
from tenacity import RetryError
from pydantic import ValidationError

from typing import Any


class KafkaConsumer:
    DLQ_TOPIC = "order-service.events.dlq"
    MAX_WORKERS = 10

    def __init__(
        self,
        handlers: KafkaEventHandlers,
        kafka_producer: IKafkaProducer,
        metrics_service: IMetricsService,
        logging_service: ILoggingService,
    ):
        self.consumer: AIOKafkaConsumer | None = None

        self.handlers = handlers
        # Topics are now derived from whatever handlers register themselves
        self.subscribed_topics = self.handlers.get_registered_topics()

        self.kafka_producer = kafka_producer
        self.metrics_service = metrics_service
        self.logger = logging_service.get_logger("KafkaConsumer")

        self.dlq_topic = self.DLQ_TOPIC

        self.executor = ThreadPoolExecutor(max_workers=self.MAX_WORKERS)

    async def is_healthy(self) -> bool:
        """Verifies connection health via public APIs."""
        try:
            if self.consumer is None:
                raise RuntimeError("Kafka consumer not started")

            await self.consumer.topics()

            assignments = self.consumer.assignment()
            if not assignments:
                pass

            return True
        except Exception:
            return False

    async def check_broker_readiness(self) -> bool:
        """Check Kafka broker readiness by bootstrapping consumer client metadata."""
        try:
            if self.consumer is None:
                raise RuntimeError("Kafka consumer not started")

            client = getattr(self.consumer, "_client", None)
            if client is None:
                await self.consumer.start()
                await self.consumer.stop()
                return True

            await client.bootstrap()
            return True
        except Exception as e:
            self.logger.error(f"Kafka broker readiness check failed: {e}")
            return False

    async def start(self):
        if self.consumer is None:
            self.consumer = AIOKafkaConsumer(
                *self.subscribed_topics,
                bootstrap_servers=settings.KAFKA_BROKER,
                group_id=settings.KAFKA_CONSUMER_GROUP or "order-service-group",
                auto_offset_reset="latest",
                enable_auto_commit=False,
                max_poll_records=settings.KAFKA_CONSUMER_MAX_POLL_RECORDS,
            )

        await self.consumer.start()
        self.logger.info(
            "Kafka Consumer started and listening for order events...")

        try:
            async for msg in self.consumer:
                try:
                    await self.handle_message(msg)
                except Exception as msg_exc:
                    self.logger.error(
                        f"Error within message handling loop: {msg_exc}")
                await self.consumer.commit()
        except Exception as e:
            self.logger.error(f"Consumer crashed: {str(e)}")
        finally:
            await self.consumer.stop()
            self.executor.shutdown(wait=False)

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
        """Routes event to its registered handler via the handler registry."""
        try:
            await self.handlers.dispatch(topic, event)

        except UnknownTopicError:
            self.logger.warning(f"Unknown topic received: {topic}")

        except ValidationError as ve:
            self.logger.error(
                f"Pydantic ValidationError for topic {topic}: {ve}")
            raise
        except OrderNotFoundException as e:
            self.logger.error(f"Order not found: {str(e)}")
            raise
        except RetryError as retry_err:
            last_exc = getattr(retry_err, 'last_attempt', None)
            error_msg = None
            if last_exc and hasattr(last_exc, 'exception') and last_exc.exception():
                err = last_exc.exception()
                error_msg = str(err)
                error_detail = f"RetryError: {error_msg}"
                self.logger.error(
                    f"RetryError while processing event for {topic}: {error_detail} | Real error: {error_msg}"
                )
            else:
                error_detail = f"RetryError: {str(retry_err)}"
                self.logger.error(
                    f"RetryError while processing event for {topic}: {error_detail}"
                )
            raise

        except Exception as e:
            self.logger.error(f"Failed to process event for {topic}: {str(e)}")

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