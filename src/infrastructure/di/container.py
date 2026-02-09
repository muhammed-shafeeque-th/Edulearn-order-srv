from dependency_injector import containers, providers
from src.application.use_cases.order.get_revenue_stats_use_case import GetRevenueStatsUseCase
from src.application.use_cases.order.restore_order_use_case import RestoreOrderUseCase
from src.application.use_cases.order.order_timeout_use_case import HandleOrderTimeoutUseCase
from src.application.use_cases.order.order_failed_use_case import OrderFailedUseCase
from src.application.use_cases.order.order_success_use_case import OrderSuccessUseCase
from src.application.use_cases.order.order_payment_initiated_use_case import OrderPaymentInitiatedUseCase
from src.application.use_cases.order.get_order_use_case import GetOrderUseCase
from src.application.use_cases.order.get_orders_use_case import GetOrdersUseCase
from src.infrastructure.grpc.clients.couser_service_client import CourseServiceClient
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from src.application.interfaces.grpc_client_interface import IUserServiceClient, ICourseServiceClient, ISessionServiceClient
from src.application.use_cases.order.place_order_use_case import PlaceOrderUseCase
from src.application.use_cases.session_booking.session_booking_use_case import BookSessionUseCase
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.tracing_interface import ITracingService
from src.application.services.saga.saga_orchestrator import SagaOrchestrator
from src.application.services.saga.steps.order_steps import CreateOrderStep, RequestPaymentStep
from src.application.services.saga.steps.session_booking_steps import CheckSessionAvailabilityStep, CreateSessionBookingStep, RequestSessionPaymentStep
from src.infrastructure.database.repositories.sql_order_repository import SqlOrderRepository
from src.infrastructure.database.repositories.sql_session_booking_repository import SqlSessionBookingRepository
from src.infrastructure.kafka.producer import KafkaProducer
from src.infrastructure.kafka.consumer import KafkaConsumer
from src.infrastructure.redis.redis_client import RedisClient
from src.infrastructure.grpc.clients.user_service_client import UserServiceClient
from src.infrastructure.grpc.clients.session_service_client import SessionServiceClient
from src.infrastructure.grpc.auth_guard import AuthGuard
from src.infrastructure.observability.logging_service import LoggingService
from src.infrastructure.observability.metrics_service import MetricsService
from src.infrastructure.observability.tracing_service import TracingService
from src.infrastructure.database.database import AsyncSessionFactory
from src.infrastructure.config.settings import settings
from src.domain.entities.order import Order
from src.domain.entities.session_booking import SessionBooking


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "src.application.use_cases.order.place_order_use_case",
        "src.application.use_cases.order.get_order_use_case",
        "src.application.use_cases.order.get_orders_use_case",
        "src.application.use_cases.session_booking.session_booking_use_case",
        "src.application.services.saga.saga_orchestrator",
        "src.application.services.saga.steps.order_steps",
        "src.application.services.saga.steps.session_booking_steps",
        "src.presentation.grpc.order_service_impl",
        "src.main",
        # Note: If you plan to use dependency injection (e.g., with `@inject`) for dependencies inside the KafkaConsumer or modules/components that the consumer calls, you should add its Python import path (e.g., "src.infrastructure.kafka.consumer") to this wiring config.
        # This will enable Dependency Injector to perform injection/wiring in that module.
        # If you do not wire it here, Dependency Injector will not automatically inject dependencies into functions/classes declared in KafkaConsumer or its module.
        # Only add modules here if you use DI features (like @inject, Provide[], etc.) within them.
    ])

    # Configuration
    config = providers.Configuration(pydantic_settings=[settings])

    # Observability Services
    logging_service = providers.Singleton(LoggingService)
    metrics_service = providers.Singleton(MetricsService)
    tracing_service = providers.Singleton(TracingService)

    # Database
    db_session_factory = providers.Factory(AsyncSessionFactory)

    # Redis
    redis_client = providers.Singleton(
        RedisClient, logger_service=logging_service)

    # Repositories
    order_repository = providers.Factory(
        SqlOrderRepository,
        # session=db_session_factory,
        redis=redis_client,
        logging_service=logging_service,
    )
    session_booking_repository = providers.Factory(
        SqlSessionBookingRepository,
        session=db_session_factory,
        redis=redis_client,
        logging_service=logging_service,
    )

    # Kafka
    kafka_producer = providers.Singleton(
        KafkaProducer,
        logging_service
    )

    # gRPC Clients
    user_service_client = providers.Singleton(
        UserServiceClient,
        logging_service=logging_service,
        token=None,
    )
    course_service_client = providers.Singleton(
        CourseServiceClient,
        logging_service=logging_service,
        token=None,
    )
    session_service_client = providers.Singleton(
        SessionServiceClient,
        logging_service=logging_service,
        token=None,
    )

    # Auth
    auth_guard = providers.Singleton(
        AuthGuard,
        user_service_client=user_service_client,
        logging_service=logging_service,
    )

    # Use Cases
    place_order_use_case = providers.Factory(
        PlaceOrderUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        user_service_client=user_service_client,
        course_service_client=course_service_client,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    get_order_use_case = providers.Factory(
        GetOrderUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    restore_order_use_case = providers.Factory(
        RestoreOrderUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    get_orders_use_case = providers.Factory(
        GetOrdersUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    payment_initiated_handler = providers.Factory(
        OrderPaymentInitiatedUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    order_success_handler = providers.Factory(
        OrderSuccessUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    order_failed_handler = providers.Factory(
        OrderFailedUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    get_revenue_stats_use_case = providers.Factory(
        GetRevenueStatsUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    book_session_use_case = providers.Factory(
        BookSessionUseCase,
        session_booking_repository=session_booking_repository,
        kafka_producer=kafka_producer,
        session_service_client=session_service_client,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    order_timeout_handler = providers.Factory(
        HandleOrderTimeoutUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )

    # Kafka consumer
    kafka_consumer = providers.Singleton(
        KafkaConsumer,
        order_repository=order_repository,
        session_booking_repository=session_booking_repository,
        payment_initiated_handler=payment_initiated_handler,
        order_success_handler=order_success_handler,
        order_failed_handler=order_failed_handler,
        order_timeout_handler=order_timeout_handler,
        kafka_producer=kafka_producer,
        metrics_service=metrics_service,
        redis=redis_client,
        # logging_service=logging_service.provided.get_logger.call("KafkaConsumer")
        logging_service=logging_service
    )

    # SAGA Orchestrator (Factory for dynamic steps, runtime objects must be passed at runtime)
    saga_orchestrator = providers.Factory(
        SagaOrchestrator,
        logging_service=logging_service,
    )
    session_saga_orchestrator = providers.Factory(
        SagaOrchestrator,
        logging_service=logging_service,
        metrics=metrics_service,
    )


# Initialize the container
container = Container()
container.wire(modules=[__name__])
