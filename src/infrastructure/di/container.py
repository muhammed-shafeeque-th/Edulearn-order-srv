from dependency_injector import containers, providers
from src.application.use_cases.order.impls.order_timeout_use_case import OrderTimeoutUseCase
from src.presentation.http.health_server import HealthServer
from src.infrastructure.grpc.order_server import OrderGrpcServer
from src.presentation.grpc.order_grpc_handlers import OrderServiceHandler
from src.presentation.kafka.kafka_handlers import KafkaEventHandlers
from src.infrastructure.observability.logger.logger_config import LoggerConfig
from src.infrastructure.observability.logger.logger_manager import LoggerManager
from src.application.use_cases.order.impls.get_revenue_stats_use_case import GetRevenueStatsUseCase
from src.application.use_cases.order.impls.restore_order_use_case import RestoreOrderUseCase
from src.application.use_cases.order.impls.order_failed_use_case import OrderFailedUseCase
from src.application.use_cases.order.impls.order_success_use_case import OrderSuccessUseCase
from src.application.use_cases.order.impls.order_payment_initiated_use_case import OrderPaymentInitiatedUseCase
from src.application.use_cases.order.impls.get_order_use_case import GetOrderUseCase
from src.application.use_cases.order.impls.get_orders_use_case import GetOrdersUseCase
from src.application.use_cases.order.impls.expire_order_use_case import ExpireOrderUseCase
from src.infrastructure.grpc.clients.couser_service_client import CourseServiceClient
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.redis_interface import IRedisService
from src.application.interfaces.grpc_client_interface import IUserServiceClient, ICourseServiceClient, ISessionServiceClient
from src.application.use_cases.order.impls.place_order_use_case import PlaceOrderUseCase
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
from src.infrastructure.observability.logger.logger_service import LoggingService
from src.infrastructure.observability.metrics.metrics_service import MetricsService
from src.infrastructure.observability.tracer.tracing_service import TracingService
from src.infrastructure.database.database import AsyncSessionFactory
from src.infrastructure.config.settings import settings
from src.domain.entities.order import Order


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=[
        "src.application.use_cases.order.impls.place_order_use_case",
        "src.application.use_cases.order.impls.get_order_use_case",
        "src.application.use_cases.order.impls.get_orders_use_case",
        "src.application.use_cases.session_booking.session_booking_use_case",
        "src.application.services.saga.saga_orchestrator",
        "src.application.services.saga.steps.order_steps",
        "src.application.services.saga.steps.session_booking_steps",
        "src.main",
        # Note: If you plan to use dependency injection (e.g., with `@inject`) for dependencies inside the KafkaConsumer or modules/components that the consumer calls, you should add its Python import path (e.g., "src.infrastructure.kafka.consumer") to this wiring config.
        # This will enable Dependency Injector to perform injection/wiring in that module.
        # If you do not wire it here, Dependency Injector will not automatically inject dependencies into functions/classes declared in KafkaConsumer or its module.
        # Only add modules here if you use DI features (like @inject, Provide[], etc.) within them.
    ])

    # Configuration
    config = providers.Configuration(pydantic_settings=[settings])
    logger_config = providers.Singleton(
        LoggerConfig,
        service_name=settings.SERVICE_NAME,
        environment=settings.ENVIRONMENT,
        # level=settings.,
        )

    logger_manager = providers.Singleton(LoggerManager, config=logger_config)

    # Observability Services
    metrics_service = providers.Singleton(MetricsService)
    tracing_service = providers.Singleton(TracingService)
    logging_service = providers.Singleton(
        LoggingService,
        logger_manager=logger_manager,
    )

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
    # book_session_use_case = providers.Factory(
    #     BookSessionUseCase,
    #     session_booking_repository=session_booking_repository,
    #     kafka_producer=kafka_producer,
    #     session_service_client=session_service_client,
    #     redis=redis_client,
    #     logging_service=logging_service,
    #     metrics_service=metrics_service,
    # )
    order_timeout_handler = providers.Factory(
        OrderTimeoutUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )
    expire_order_use_case = providers.Factory(
        ExpireOrderUseCase,
        order_repository=order_repository,
        kafka_producer=kafka_producer,
        redis=redis_client,
        logging_service=logging_service,
        metrics_service=metrics_service,
    )

    # Request handlers
    
    kafka_handlers = providers.Singleton(
        KafkaEventHandlers,
        payment_initiated_handler=payment_initiated_handler,
        order_success_handler=order_success_handler,
        order_failed_handler=order_failed_handler,
        order_timeout_handler=order_timeout_handler,
    )
    
    order_grpc_handlers = providers.Singleton(
            OrderServiceHandler,
            place_order_use_case=place_order_use_case,
            get_orders_use_case=get_orders_use_case,
            get_revenue_stats_use_case=get_revenue_stats_use_case,
            get_order_use_case=get_order_use_case,
            restore_order_use_case=restore_order_use_case,
            logger=logging_service,
            # book_session_use_case=book_session_use_case,
        )
    
    # server impl
    order_grpc_server = providers.Singleton(
            OrderGrpcServer,
            grpc_handlers=order_grpc_handlers,
            auth_guard=auth_guard,
            logger_service=logging_service,
            metrics=metrics_service,
            tracer=tracing_service,
        )
    kafka_consumer = providers.Singleton(
            KafkaConsumer,
            handlers=kafka_handlers,
            kafka_producer=kafka_producer,
            logging_service=logging_service,
            metrics_service=metrics_service,
        )
    health_server = providers.Singleton(
            HealthServer,
            logger=logging_service,
            kafka=kafka_consumer,
            redis=redis_client,
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
