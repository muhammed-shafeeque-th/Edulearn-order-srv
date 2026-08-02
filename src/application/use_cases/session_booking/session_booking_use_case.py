from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.grpc_client_interface import ISessionServiceClient
from src.domain.repositories.session_booking_repository import ISessionBookingRepository
from src.application.dtos.session_booking_create_dto import SessionBookingCreateDTO
from src.application.dtos.session_booking_dto import SessionBookingDTO
from src.domain.entities.session_booking import SessionBooking
from src.domain.value_objects.money import Money
from src.application.services.saga.saga_orchestrator import SagaOrchestrator
from src.application.services.saga.steps.session_booking_steps import CheckSessionAvailabilityStep, CreateSessionBookingStep, RequestSessionPaymentStep
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from tenacity import retry, stop_after_attempt, wait_exponential
import json

class BookSessionUseCase:
    def __init__(
        self,
        session_booking_repository: ISessionBookingRepository,
        kafka_producer: IKafkaProducer,
        session_service_client: ISessionServiceClient,
        redis: IRedisService,
        logging_service: ILoggingService,
        metrics_service: IMetricsService,
    ):
        self.session_booking_repository = session_booking_repository
        self._kafka_producer = kafka_producer
        self.session_service_client = session_service_client
        self._cache = redis
        self._logger = logging_service.get_logger("BookSessionUseCase")
        self._metrics = metrics_service

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def execute(self, booking_dto: SessionBookingCreateDTO) -> SessionBookingDTO:
        self._logger.info(f"Executing BookSessionUseCase for user {booking_dto.user_id} and session {booking_dto.session_id}")

        # Check cache for session details
        cache_key = f"session:{booking_dto.session_id}"
        cached_session = await self._cache.get(cache_key)
        if cached_session:
            session = json.loads(cached_session)
            self._logger.debug(f"Cache hit for session {booking_dto.session_id}")
            self._metrics.cache_hits(type="session")
        else:
            session = await self.session_service_client.get_session(booking_dto.session_id)
            if not session:
                self._logger.error(f"Session {booking_dto.session_id} not found")
                raise ValueError(f"Session {booking_dto.session_id} not found")
            await self._cache.set(cache_key, json.dumps(session), 3600)
            self._logger.debug(f"Cache miss for session {booking_dto.session_id}, cached session")
            self._metrics.cache_misses(type="session")

        max_slots = session["max_slots"]
        amount = session["price"]

        # Create booking
        booking = SessionBooking.create(
            user_id=booking_dto.user_id,
            session_id=booking_dto.session_id,
            amount=Money(amount=amount),
        )

        # Execute SAGA
        saga = SagaOrchestrator(
            steps=[
                CheckSessionAvailabilityStep(self.session_service_client, booking_dto.session_id, max_slots),
                CreateSessionBookingStep(booking, self.session_booking_repository, self._cache),
                RequestSessionPaymentStep(self._kafka_producer),
            ],
            logging_service=self._logger,
            metrics=self._metrics,
        )
        await saga.execute()

        # Invalidate cache for session bookings
        await self._cache.client.delete(f"session_bookings:{booking_dto.session_id}")
        self._logger.debug(f"Invalidated session bookings cache for session {booking_dto.session_id}")

        return SessionBookingDTO(
            id=booking.id,
            user_id=booking.user_id,
            session_id=booking.session_id,
            amount=booking.amount.amount,
            currency=booking.amount.currency,
            status=booking.status,
            created_at=booking.created_at,
            updated_at=booking.updated_at,
        )