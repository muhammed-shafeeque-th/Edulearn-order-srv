# Order Service - Overview

## Purpose

The Order Service manages orders and session bookings in the EduLearn platform. It handles order creation, lifecycle management, and coordinates with payment and course services.

## Scope & Responsibilities

### Core Responsibilities

1. **Order Management**
   - Create orders
   - Update order status
   - Order lifecycle management
   - Order cancellation
   - Order expiration handling

2. **Session Bookings**
   - Book sessions
   - Manage session bookings
   - Session lifecycle

3. **Order State Management**
   - Order status transitions
   - State validation
   - Idempotent operations

4. **Event Publishing**
   - Publishes order lifecycle events
   - Events: OrderCreated, OrderSucceeded, OrderFailed, etc.

5. **Integration**
   - Coordinates with Payment Service
   - Validates with Course Service
   - Integrates with User Service

## Folder Structure

```
order/
├── src/                          # Source code
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   ├── application/             # Application layer
│   │   ├── dtos/                # Data Transfer Objects
│   │   │   ├── base_event_dto.py         # Base event DTO
│   │   │   ├── get_order_dto.py          # Order retrieval DTO
│   │   │   ├── get_orders_by_user_dto.py # User orders DTO
│   │   │   ├── order_create_dto.py       # Order creation DTO
│   │   │   ├── order_dto.py              # Order DTO
│   │   │   ├── order_payment_failure_dto.py # Payment failure DTO
│   │   │   ├── order_payment_initiate_dto.py # Payment init DTO
│   │   │   ├── order_payment_timeout_dto.py # Payment timeout DTO
│   │   │   ├── order_success_dto.py      # Order success DTO
│   │   │   └── session_booking_create_dto.py # Session booking DTO
│   │   ├── events/              # Event definitions
│   │   │   └── order/           # Order event definitions
│   │   ├── interfaces/          # Interface definitions
│   │   │   ├── auth_guard_interface.py   # Authentication interface
│   │   │   ├── grpc_client_interface.py  # gRPC client interface
│   │   │   ├── kafka_producer_interface.py # Kafka producer interface
│   │   │   ├── logging_interface.py      # Logging interface
│   │   │   ├── metrics_interface.py      # Metrics interface
│   │   │   └── redis_interface.py        # Redis interface
│   │   ├── services/            # Application services
│   │   │   ├── interfaces/      # Service interfaces
│   │   │   └── saga/            # Saga pattern implementation
│   │   └── use_cases/           # Business use cases
│   │       ├── order/           # Order use cases
│   │       │   ├── create_order_use_case.py     # Order creation
│   │       │   ├── get_order_use_case.py        # Order retrieval
│   │       │   ├── get_orders_by_user_use_case.py # User orders
│   │       │   ├── update_order_status_use_case.py # Status updates
│   │       │   └── cancel_order_use_case.py     # Order cancellation
│   │       └── session_booking/ # Session booking use cases
│   │           └── create_session_booking_use_case.py # Session booking
│   ├── domain/                  # Domain layer
│   │   ├── entities/            # Domain entities
│   │   │   ├── order_items.py   # Order item domain model
│   │   │   ├── order.py         # Order domain model
│   │   │   ├── payment_details.py # Payment details model
│   │   │   └── session_booking.py # Session booking model
│   │   ├── events/              # Domain events
│   │   │   ├── base_event.py    # Base event class
│   │   │   ├── order_create_event.py # Order creation event
│   │   │   ├── order_failed_event.py # Order failure event
│   │   │   └── order_success_event.py # Order success event
│   │   ├── exceptions/          # Domain exceptions
│   │   │   └── exceptions.py    # Custom exceptions
│   │   ├── repositories/        # Repository interfaces
│   │   │   ├── order_repository.py       # Order repository interface
│   │   │   └── session_booking_repository.py # Session booking interface
│   │   └── value_objects/       # Value objects
│   │       └── money.py         # Money value object
│   ├── infrastructure/          # Infrastructure layer
│   │   ├── api/                 # API layer (optional)
│   │   │   └── main.old.py      # Old API implementation
│   │   ├── cache/               # Caching implementation
│   │   │   └── cache_service.py # Redis cache service
│   │   ├── config/              # Configuration
│   │   │   └── settings.py      # Application settings
│   │   ├── database/            # Database implementation
│   │   │   ├── database.py      # Database connection
│   │   │   ├── mapper.py        # Data mappers
│   │   │   ├── mappers/         # Entity mappers
│   │   │   └── models/          # SQLAlchemy models
│   │   ├── di/                  # Dependency injection
│   │   │   ├── container.py     # DI container
│   │   │   └── dependencies.py  # Dependencies setup
│   │   ├── grpc/                # gRPC implementation
│   │   │   ├── clients/         # gRPC client implementations
│   │   │   ├── interceptors/    # gRPC interceptors
│   │   │   ├── middleware/      # gRPC middleware
│   │   │   └── services/        # gRPC service implementations
│   │   ├── kafka/               # Kafka implementation
│   │   │   ├── consumer.py      # Kafka consumer
│   │   │   ├── producer.py      # Kafka producer
│   │   │   └── topics.py        # Topic definitions
│   │   ├── observability/       # Monitoring and observability
│   │   │   ├── logging/         # Logging setup
│   │   │   ├── metrics/         # Metrics collection
│   │   │   ├── tracing/         # Distributed tracing
│   │   │   └── health/          # Health checks
│   │   └── redis/               # Redis implementation
│   │       └── redis_service.py # Redis service
│   ├── presentation/            # Presentation layer
│   │   └── grpc/                # gRPC controllers
│   │       ├── order_service.py # Order gRPC service
│   │       └── session_service.py # Session gRPC service
│   └── shared/                  # Shared utilities
│       ├── events/              # Shared event definitions
│       └── utils/               # Utility functions
├── proto/                      # Protocol buffer definitions
│   ├── course_service.proto     # Course service protobuf
│   ├── order_service.proto      # Order service protobuf
│   ├── session_service.proto    # Session service protobuf
│   ├── user_service.proto       # User service protobuf
│   └── course/                  # Course-related protobufs
├── migrations/                  # Database migrations
│   ├── __env.py                # Migration environment
│   ├── env.py                  # Migration configuration
│   ├── script.py.mako          # Migration script template
│   └── versions/               # Migration versions
├── tests/                       # Test files
│   ├── conftest.py             # Test configuration
│   ├── integration/            # Integration tests
│   │   └── test_order_service.py # Order service integration tests
│   └── unit/                   # Unit tests
│       ├── application/        # Application layer tests
│       ├── domain/             # Domain layer tests
│       └── infrastructure/     # Infrastructure layer tests
├── requirements.txt            # Python dependencies
├── pyrightconfig.json          # Pyright type checker config
├── task.py                     # Task runner configuration
├── util.txt                    # Utility scripts
├── Dockerfile                  # Docker configuration
├── docker-compose.yaml         # Docker compose for development
├── alembic.ini                 # Database migration configuration
├── Makefile                    # Make commands
├── prometheus.yaml             # Prometheus configuration
├── env.example                 # Environment variables template
├── LICENSE                     # License
└── README.md                   # Service documentation
```

### Out of Scope

- Payment processing (Payment Service)
- Course management (Course Service)
- User management (User Service)

## Key Features

- **Order Lifecycle**: Complete order state machine
- **Idempotency**: Safe order creation
- **Async Operations**: Async database operations
- **Event-Driven**: Publishes events for downstream services
- **Session Bookings**: Session booking management

## Service Boundaries

### Owns Data For

- Orders
- Order items
- Session bookings
- Payment details (references)

### Depends On

- **Payment Service** (via gRPC): Payment processing
- **Course Service** (via gRPC): Course validation
- **User Service** (via gRPC): User validation
- **Database**: PostgreSQL for persistence
- **Redis**: Caching
- **Kafka**: Event publishing

## Technical Stack

- **Framework**: FastAPI
- **Language**: Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Cache**: Redis
- **Messaging**: Kafka
- **RPC**: gRPC
- **Migrations**: Alembic

## Key Entities

- **Order**: Order aggregate root
- **OrderItem**: Order line items
- **PaymentDetails**: Payment information
- **SessionBooking**: Session booking records

