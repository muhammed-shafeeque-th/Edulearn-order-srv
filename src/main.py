import sys
import os

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from sqlalchemy import text
import asyncio
from prometheus_client import make_asgi_app
from src.infrastructure.observability.metrics_service import MetricsService
from src.application.interfaces.tracing_interface import ITracingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.logging_interface import ILoggingService
from src.infrastructure.redis.redis_client import RedisClient
from src.infrastructure.grpc.clients.user_service_client import UserServiceClient
from src.application.use_cases.order.place_order_use_case import PlaceOrderUseCase
from src.infrastructure.database.database import get_db, AsyncSession
from src.presentation.grpc.order_server import start_grpc_server
from src.infrastructure.di.container import Container
from src.infrastructure.config.settings import settings
import logging
from fastapi import FastAPI, Depends, HTTPException
import uvicorn
from contextlib import asynccontextmanager



# Initialize container
container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Start Kafka producer
        kafka_producer = container.kafka_producer()
        await kafka_producer.start()

        # Start Kafka consumer
        kafka_consumer = container.kafka_consumer()
        asyncio.create_task(kafka_consumer.start())

        # Start gRPC server
        auth_guard = container.auth_guard()
        logging_service = container.logging_service()
        metrics_service = container.metrics_service()
        tracing_service = container.tracing_service()
        asyncio.create_task(
            start_grpc_server(
                place_order_use_case=container.place_order_use_case(),
                get_orders_use_case=container.get_orders_use_case(),
                get_revenue_stats_use_case=container.get_revenue_stats_use_case(),
                get_order_use_case=container.get_order_use_case(),
                restore_order_use_case=container.restore_order_use_case(),
                book_session_use_case=container.book_session_use_case(),
                auth_guard=auth_guard,
                logger_service=logging_service,
                metrics=metrics_service,
                tracer=tracing_service,
            )
        )

        async with get_db() as session:
            pass
            # result = await session.execute(text("SELECT COUNT(*) FROM orders WHERE status = 'PENDING' OR status = 'COMPLETED'"))
            # count = result.scalar()
            # metrics_service.active_orders(count or 0)

        yield

    except Exception as e:
        logging.exception(f"Lifespan startup error: {e}")
        os._exit(1)
    finally:
        # Shutdown
        try:
            kafka_producer = container.kafka_producer()
            await kafka_producer.stop()
            await container.redis_client().close()
        except Exception as e:
            logging.exception(f"Lifespan shutdown error: {e}")
            # Optionally exit with error code
            os._exit(1)

app = FastAPI(title="Order Service", lifespan=lifespan)

container.logging_service().setup_logger()
container.tracing_service().setup_tracing()
container.tracing_service().instrument_app(app=app)

# Prometheus metrics endpoint
app.mount("/metrics", make_asgi_app())


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db), logging_service: ILoggingService = Depends(lambda: container.logging_service())):
    try:
        await db.execute(text("SELECT 1"))
        await container.redis_client().client.ping()
        return {"status": "healthy", "database": "ok", "redis": "ok"}
    except Exception as e:
        logging_service.get_logger("HealthCheck").error(
            f"Health check failed: {str(e)}")
        # os._exit(1)
        raise HTTPException(status_code=503, detail="Service Unhealthy")

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0",
                port=settings.API_PORT, log_level=logging.INFO, reload=False)
