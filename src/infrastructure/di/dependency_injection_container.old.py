from typing import TypeVar, Type
from analytics.src.domain.interfaces.course_client import CourseServiceClient
from src.application.use_cases.session_booking.session_booking_use_case import BookSessionUseCase
from src.infrastructure.grpc.auth_guard import AuthGuard
from src.domain.repositories.order_repository import  IOrderRepository
from src.domain.repositories.session_booking_repository import  ISessionBookingRepository
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.grpc_client_interface import ICourseServiceClient, ISessionServiceClient, IUserServiceClient
from order.src.application.use_cases.order.impls.place_order_use_case import PlaceOrderUseCase
from src.application.interfaces.redis_interface import IRedisService
from src.infrastructure.database.repositories.sql_order_repository import SqlOrderRepository
from src.infrastructure.database.repositories.sql_session_booking_repository import SqlSessionBookingRepository
from src.infrastructure.kafka.producer import KafkaProducer
from src.infrastructure.grpc.clients.session_service_client import SessionServiceClient
from src.infrastructure.grpc.clients.user_service_client import UserServiceClient
from src.infrastructure.redis.redis_client import RedisClient
import logging

T = TypeVar('T')

class Container:
    def __init__(self):
        self._registry = {}
        self._instances = {}
        self.logger = logging.getLogger("Container")

    def register(self, abstraction: Type[T], implementation: Type[T]):
        self._registry[abstraction] = implementation

    def get(self, abstraction: Type[T]) -> T:
        if abstraction not in self._instances:
            implementation = self._registry.get(abstraction)
            if not implementation:
                raise ValueError(f"No implementation registered for {abstraction}")

            if abstraction == IKafkaProducer:
                self._instances[abstraction] = implementation(logger=logging.getLogger("KafkaProducer"))
            elif abstraction == IUserServiceClient:
                self._instances[abstraction] = implementation(
                    logger=logging.getLogger("UserServiceClient"),
                    token=None,  # Token can be set dynamically if needed
                )
            elif abstraction in (ICourseServiceClient, ISessionServiceClient):
                self._instances[abstraction] = implementation(
                    logger=logging.getLogger(abstraction.__name__),
                    token=None,
                )
            elif abstraction == AuthGuard:
                self._instances[abstraction] = implementation(
                    user_service_client=self.get(IUserServiceClient),
                    logger=logging.getLogger("AuthGuard"),
                )
            elif abstraction == PlaceOrderUseCase:
                self._instances[abstraction] = implementation(
                    order_repository=self.get(IOrderRepository),
                    kafka_producer=self.get(IKafkaProducer),
                    course_service_client=self.get(ICourseServiceClient),
                    redis=self.get(IRedisService),
                    logger=logging.getLogger("PlaceOrderUseCase"),
                )
            elif abstraction == BookSessionUseCase:
                self._instances[abstraction] = implementation(
                    session_booking_repository=self.get(ISessionBookingRepository),
                    kafka_producer=self.get(IKafkaProducer),
                    session_service_client=self.get(ISessionServiceClient),
                    redis=self.get(IRedisService),
                    logger=logging.getLogger("BookSessionUseCase"),
                )
            else:
                self._instances[abstraction] = implementation()
        return self._instances[abstraction]

container = Container()

# Register dependencies
container.register(IOrderRepository, SqlOrderRepository)
container.register(ISessionBookingRepository, SqlSessionBookingRepository)
container.register(IKafkaProducer, KafkaProducer)
container.register(ICourseServiceClient, CourseServiceClient)
container.register(ISessionServiceClient, SessionServiceClient)
container.register(IUserServiceClient, UserServiceClient)
container.register(IRedisService, RedisClient)
container.register(PlaceOrderUseCase, PlaceOrderUseCase)
container.register(BookSessionUseCase, BookSessionUseCase)
container.register(AuthGuard, AuthGuard)