from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any
import fastavro

from src.domain.repositories.order_repository import IOrderRepository
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.services.interfaces.saga_step import SagaStep
from src.domain.entities.order import Order

# Load avro schemas
order_schema_path = (
    Path(__file__).parent.parent.parent.parent.parent / "schemas" / "order.avsc"
)
with open(order_schema_path, "r") as f:
    order_avro_schema = fastavro.parse_schema(json.load(f))


payment_schema_path = (
    Path(__file__).parent.parent.parent.parent.parent /
    "schemas" / "payment.avsc"
)
with open(payment_schema_path, "r") as f:
    payment_avro_schema = fastavro.parse_schema(json.load(f))


class CreateOrderStep(SagaStep):
    def __init__(
        self, order: Order, order_repository: IOrderRepository
    ) -> None:
        self.order = order
        self.order_repository = order_repository

    async def execute(self, context: dict[str, Any]) -> None:
        await self.order_repository.save(self.order)
        context["order_id"] = self.order.id
        context["timestamp"] = self.order.created_at.isoformat()

    async def compensate(self, context: dict[str, Any]) -> None:
        order = await self.order_repository.find_by_id(context["order_id"])
        if order:
            order.mark_failed()
            await self.order_repository.save(order)


class RequestPaymentStep(SagaStep):
    def __init__(self, kafka_producer: IKafkaProducer) -> None:
        self.kafka_producer = kafka_producer

    async def execute(self, context: dict[str, Any]) -> None:
        order_id = context["order_id"]
        payment_event = {
            "eventType": "PaymentRequested",
            "orderId": order_id,
            "status": "PENDING",
            "transactionId": "",
            "timestamp": context.get("timestamp", datetime.now(timezone.utc).isoformat()),
        }
        await self.kafka_producer.publish_event(
            "payment-service.payment.requested", payment_event, payment_avro_schema
        )

    async def compensate(self, context: dict[str, Any]) -> None:
        order_id = context["order_id"]
        payment_event = {
            "eventType": "PaymentCancelled",
            "orderId": order_id,
            "status": "CANCELLED",
            "transactionId": "",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        await self.kafka_producer.publish_event(
            "payment-service.payment.cancelled", payment_event, payment_avro_schema
        )
