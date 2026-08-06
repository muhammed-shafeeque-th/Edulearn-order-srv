# Order Service

The **Order Service** is the transaction orchestration service of the Edulearn platform. It manages the complete lifecycle of orders and session bookings, coordinates payment workflows, validates course purchases, and ensures consistency across distributed services using **event-driven architecture** and the **Saga pattern**.

The service is built with **Python**, **FastAPI**, **gRPC**, and **Clean Architecture**, and integrates with PostgreSQL, Redis, Kafka, and OpenTelemetry-based observability infrastructure.

---

## Overview

The Order Service is the authoritative owner of order-related data within the platform. It creates and manages orders, coordinates payment initiation, validates order state transitions, and publishes domain events consumed by other services.

### Responsibilities

* Order creation
* Order lifecycle management
* Order cancellation
* Order expiration handling
* Session booking management
* Payment workflow orchestration
* Distributed transaction coordination
* Idempotent order processing
* Kafka event publishing
* Cross-service validation

### Out of Scope

* Payment processing (Payment Service)
* Course management (Course Service)
* User profile management (User Service)
* Notification delivery (Notification Service)

---

# Architecture

This service follows **Clean Architecture** with **SOLID principles**, enabling framework-independent business logic, asynchronous processing, and reliable distributed transaction coordination.

## Layered Architecture

```text
              gRPC Services
                    │
            Application Layer
   (Use Cases / Saga / DTOs / Events)
                    │
               Domain Layer
(Entities / Repositories / Value Objects)
                    │
          Infrastructure Layer
(PostgreSQL / Redis / Kafka / gRPC / Observability)
```

### Layers

#### Presentation Layer

* gRPC services
* Request validation
* Response mapping
* Transport-specific concerns

#### Application Layer

* Order use cases
* Session booking workflows
* Saga orchestration
* Event publishing
* Idempotency coordination

#### Domain Layer

* Order aggregate
* Order items
* Payment details
* Session booking
* Value objects
* Repository interfaces
* Domain events

#### Infrastructure Layer

* PostgreSQL persistence
* Redis caching
* Kafka producer/consumer
* gRPC client/server implementations
* Structured logging
* Metrics and distributed tracing

---

# Technology Stack

| Category     | Technology               |
| ------------ | ------------------------ |
| Language     | Python 3.11+             |
| Framework    | FastAPI                  |
| Architecture | Clean Architecture       |
| RPC          | gRPC                     |
| Database     | PostgreSQL               |
| ORM          | SQLAlchemy (Async)       |
| Migrations   | Alembic                  |
| Cache        | Redis                    |
| Messaging    | Kafka                    |
| Logging      | structlog                |
| Metrics      | Prometheus               |
| Tracing      | OpenTelemetry            |
| Deployment   | Docker, Kubernetes, Helm |

---

# Core Domain

The Order Service owns the transaction domain.

## Order

* Order lifecycle
* Payment status
* Purchase metadata
* User association
* Pricing information

## Order Item

* Course references
* Quantity
* Pricing snapshot
* Purchase metadata

## Payment Details

* Payment provider reference
* Transaction metadata
* Payment status
* External identifiers

## Session Booking

* Instructor sessions
* Scheduling metadata
* Booking lifecycle
* Reservation state

---

# Order Lifecycle

Orders follow a controlled state machine.

```text
PENDING
   │
   ▼
PAYMENT_INITIATED
   │
   ▼
PAYMENT_PROCESSING
   │
   ├──────────────┐
   ▼              ▼
COMPLETED      FAILED
   │              │
   ▼              ▼
FULFILLED     CANCELLED
```

State transitions are validated centrally to prevent invalid or duplicate operations.

---

# Distributed Transaction Flow

The Order Service coordinates payments using a **Saga pattern**.

```text
Create Order
      │
      ▼
Validate User
      │
      ▼
Validate Course
      │
      ▼
Initiate Payment
      │
      ▼
Payment Service
      │
      ▼
Payment Result Event
      │
      ▼
Update Order Status
      │
      ▼
Publish OrderCompleted
```

If payment fails or times out, compensating actions update the order to a consistent terminal state.

---

# Project Structure

```text
src/
├── application/
│   ├── dtos/
│   ├── use_cases/
│   ├── services/
│   └── events/
├── domain/
│   ├── entities/
│   ├── repositories/
│   ├── value_objects/
│   └── events/
├── infrastructure/
│   ├── database/
│   ├── grpc/
│   ├── kafka/
│   ├── redis/
│   ├── cache/
│   └── observability/
├── presentation/
│   └── grpc/
└── shared/
```

---

# Communication

## gRPC APIs

The Order Service exposes internal gRPC APIs consumed by:

* API Gateway
* Payment Service
* Course Service
* User Service
* Notification Service

Example operations:

* CreateOrder
* GetOrder
* GetOrdersByUser
* UpdateOrderStatus
* CancelOrder
* CreateSessionBooking
* GetSessionBooking

---

## Kafka Integration

The Order Service coordinates asynchronous workflows through Kafka.

### Published Events

| Topic                      | Purpose         |
| -------------------------- | --------------- |
| order.created.v1           | Order created   |
| order.payment.initiated.v1 | Payment started |
| order.payment.timeout.v1   | Payment timeout |
| order.completed.v1         | Order completed |
| order.failed.v1            | Order failed    |
| order.cancelled.v1         | Order cancelled |
| session.booking.created.v1 | Session booked  |

### Consumed Events

| Topic                | Purpose                     |
| -------------------- | --------------------------- |
| payment.completed.v1 | Complete order              |
| payment.failed.v1    | Fail order                  |
| payment.timeout.v1   | Expire order                |
| course.updated.v1    | Synchronize course metadata |
| user.updated.v1      | Synchronize user metadata   |

This event-driven architecture enables reliable asynchronous coordination across services.

---

# Data Ownership

The Order Service is the single source of truth for transaction-related data.

| Entity           | Owner         |
| ---------------- | ------------- |
| orders           | Order Service |
| order_items      | Order Service |
| payment_details  | Order Service |
| session_bookings | Order Service |

Other services interact with this data through gRPC APIs or Kafka events rather than direct database access.

---

# Idempotency

Order creation and payment callbacks are **idempotent**.

Strategies include:

* Idempotency keys
* Redis-backed request tracking
* Duplicate event detection
* Transaction-safe state transitions
* Safe retry support

This ensures reliable processing even during retries or network failures.

---

# Observability

The service follows the platform-wide observability architecture based on **OpenTelemetry**, **Prometheus**, **Grafana**, **Loki**, and **Tempo**.

## Logging

* Structured JSON logs
* structlog
* Correlation IDs
* Trace-aware logging
* Saga execution diagnostics

## Metrics

Prometheus metrics include:

* Order creation rate
* Order completion rate
* Payment failure rate
* Saga duration
* Order processing latency
* Kafka consumer lag
* gRPC request latency
* Cache hit/miss ratio

Exposed at:

```text
/metrics
```

## Distributed Tracing

OpenTelemetry instrumentation provides end-to-end transaction tracing.

Trace flow:

```text
API Gateway
      │
      ▼
Order Service
      │
      ▼
User / Course / Payment Services
      │
      ▼
PostgreSQL / Redis / Kafka
```

Traces are exported to **OTEL Collector → Tempo → Grafana**.

---

# Redis Usage

Redis is used for:

* Idempotency keys
* Order caching
* Temporary transaction state
* Duplicate request prevention
* Retry coordination
* Distributed workflow support

---

# Database

PostgreSQL is the primary persistent datastore.

SQLAlchemy (Async) manages:

* Entity mapping
* Repository implementations
* Async transactions
* Connection pooling

Alembic manages schema migrations.

Typical migration command:

```bash
alembic upgrade head
```

---

# Local Development

## Prerequisites

* Python 3.11+
* PostgreSQL
* Redis
* Kafka

## Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Migrations

```bash
alembic upgrade head
```

## Start Development Server

```bash
python -m src.main
```

---

# Environment Variables

| Variable                    | Description                  |
| --------------------------- | ---------------------------- |
| DATABASE_URL                | PostgreSQL connection string |
| REDIS_URL                   | Redis connection string      |
| KAFKA_BROKERS               | Kafka broker list            |
| USER_SERVICE_GRPC_URL       | User Service endpoint        |
| COURSE_SERVICE_GRPC_URL     | Course Service endpoint      |
| PAYMENT_SERVICE_GRPC_URL    | Payment Service endpoint     |
| OTEL_EXPORTER_OTLP_ENDPOINT | OTLP collector endpoint      |
| LOG_LEVEL                   | Logging level                |

See `env.example` for the complete configuration.

---

# Docker

The service uses a **multi-stage Docker build** optimized for production.

Optimizations include:

* Multi-stage builds
* Minimal runtime image
* Non-root execution
* Layer caching
* Reduced attack surface

---

# Kubernetes Deployment

Deployment is managed through the **Edulearn umbrella Helm chart**.

The service is deployed with:

* ClusterIP service
* gRPC exposure
* Liveness probes
* Readiness probes
* Resource requests and limits
* Horizontal Pod Autoscaler support
* Prometheus ServiceMonitor

---

# CI/CD

This service participates in the platform GitOps deployment pipeline.

```text
Git Push
    │
    ▼
GitHub Actions
    ├── Test
    ├── Build
    ├── Lint
    ├── Trivy Scan
    └── Push to GHCR
             │
             ▼
ArgoCD Image Updater
             │
             ▼
ArgoCD
             │
             ▼
Amazon EKS
```

---

# Performance Optimizations

Implemented optimizations include:

* Async SQLAlchemy operations
* Connection pooling
* Redis caching
* Kafka asynchronous processing
* Idempotent request handling
* Efficient repository queries
* Optimized Docker image size

---

# Security

The service follows production-oriented security practices.

## Transaction Security

* Idempotent payment handling
* State transition validation
* Distributed transaction consistency
* Secure gRPC communication
* Internal service authentication

## Secrets Management

Production deployments retrieve secrets from:

* AWS Secrets Manager
* External Secrets Operator

## Container Security

* Runs as non-root user
* No shell access
* Minimal Linux capabilities
* Read-only filesystem where applicable

---

# Testing

```bash
# Unit tests
pytest tests/unit

# Integration tests
pytest tests/integration

# End-to-end tests
pytest tests/e2e

# Coverage
pytest --cov=src
```

---

# Related Repositories

| Repository                    | Description                                                   |
| ----------------------------- | ------------------------------------------------------------- |
| [edulearn-platform](https://github.com/muhammed-shafeeque-th/edulearn-platform)             | Platform orchestration repository                             |
| [edulearn-api-gateway](https://github.com/muhammed-shafeeque-th/edulearn-api-gateawy)          | API Gateway                                                   |
| [edulearn-user-service](https://github.com/muhammed-shafeeque-th/edulearn-user-srv)         | User profile service                                          |
| [edulearn-course-service](https://github.com/muhammed-shafeeque-th/edulearn-course-srv)       | Course management service                                     |
| [edulearn-payment-service](https://github.com/muhammed-shafeeque-th/edulearn-payment-srv)      | Payment processing service                                    |
| [edulearn-auth-service](https://github.com/muhammed-shafeeque-th/edulearn-auth-srv)      | Authentication service                                    |
| [edulearn-client](https://github.com/muhammed-shafeeque-th/edulearn-client)        | Edulearn Frontend                                      |
| [edulearn-notification-service](https://github.com/muhammed-shafeeque-th/edulearn-notification-srv) | Notification service                                          |
| [edulearn-auth-service](https://github.com/muhammed-shafeeque-th/edulearn-auth-srv)         | Authentication service                                        |
| [@edulearn/core](https://github.com/muhammed-shafeeque-th/edulearn-core)                | Shared logging, metrics, tracing, Redis, Kafka, health checks |
| [@edulearn/nest](https://github.com/muhammed-shafeeque-th/edulearn-nest)                | Shared NestJS infrastructure package                          |

---

# License

This project is part of the **Edulearn Platform** and is licensed under the MIT [License](./LICENSE).
