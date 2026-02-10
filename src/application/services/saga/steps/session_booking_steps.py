from datetime import datetime
import json
from datetime import timezone
from pathlib import Path
from typing import Any
import fastavro
import io


from src.application.interfaces.grpc_client_interface import (
    ISessionServiceClient,
)
from src.application.interfaces.redis_interface import IRedisService
from src.domain.exceptions.exceptions import SessionNotFoundException
from src.domain.repositories.session_booking_repository import (
    ISessionBookingRepository,
)
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.services.interfaces.saga_step import SagaStep
from src.domain.entities.session_booking import SessionBooking
from src.infrastructure.redis.redis_client import RedisClient


payment_schema_path = (
    Path(__file__).parent.parent.parent.parent.parent
    / "schemas"
    / "payment.avsc"
)
with open(payment_schema_path, "r") as f:
    payment_avro_schema = fastavro.parse_schema(json.load(f))

    class CheckSessionAvailabilityStep(SagaStep):
        def __init__(
            self,
            session_service_client: ISessionServiceClient,
            session_id: str,
            max_slots: int,
        ) -> None:
            self.session_service_client = session_service_client
            self.session_id = session_id
            self.max_slots = max_slots

        async def execute(self, context: dict[str, Any]) -> None:
            available_slots = await self.session_service_client.get_available_slots(
                self.session_id
            )
            if available_slots <= 0:
                raise ValueError(f"No available slots for session {self.session_id}")
            context["available_slots"] = available_slots
            context["max_slots"] = self.max_slots

        async def compensate(self, context: dict[str, Any]) -> None:
            pass # No compensation needed for a read operation

    class CreateSessionBookingStep(SagaStep):
        def __init__(
            self,
            booking: SessionBooking,
            session_booking_repository: ISessionBookingRepository,
            redis_client: IRedisService,
        ) -> None:
            self.booking = booking
            self.session_booking_repository = session_booking_repository
            self.redis_client = redis_client

        async def execute(self, context: dict[str, Any]) -> None:
            lock_key = f"lock:session:{self.booking.session_id}"

            async with self.redis_client.lock(lock_key, timeout=10):
                current_bookings = await self.session_booking_repository.count_bookings_for_session(self.booking.session_id)
                max_slots = context.get("max_slots", 10)
                if current_bookings >= max_slots:
                    raise ValueError(
                        f"Session {self.booking.session_id} is fully booked"
                    )

                await self.session_booking_repository.save(self.booking)
                context["booking_id"] = self.booking.id

        async def compensate(self, context: dict[str, Any]) -> None:
            if booking_id := context.get("booking_id"):
                booking = await self.session_booking_repository.find_by_id(
                    booking_id=booking_id
                )
                if not booking:
                    raise SessionNotFoundException(f"Session booking not found with booking Id {booking_id}")
                booking.cancel()
                await self.session_booking_repository.save(booking)

    class RequestSessionPaymentStep(SagaStep):
        def __init__(self, kafka_producer: IKafkaProducer) -> None:
            self.kafka_producer = kafka_producer

        async def execute(self, context: dict[str, Any]) -> None:
            booking_id = context["booking_id"]
            payment_event = {
                "eventType": "SessionPaymentRequested",
                "orderId": booking_id,
                "status": "PENDING",
                "transactionId": "",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            await self.kafka_producer.publish_event(
                "payment-service.session_payment.requested", payment_event, payment_avro_schema
            )

        async def compensate(self, context: dict[str, Any]) -> None:
            booking_id = context["booking_id"]
            payment_event = {
                "eventType": "SessionPaymentCancelled",
                "orderId": booking_id,
                "status": "CANCELLED",
                "transactionId": "",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            await self.kafka_producer.publish_event(
                "payment-service.session_payment.cancelled", payment_event, payment_avro_schema
            )
