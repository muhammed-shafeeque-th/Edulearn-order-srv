import sys
import os


# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



from sqlalchemy import text
import asyncio
from prometheus_client import make_asgi_app
from src.application.interfaces.logging_interface import ILoggingService
from src.application.use_cases.order.impls.place_order_use_case import PlaceOrderUseCase
from src.infrastructure.database.database import db as database, get_db, AsyncSession
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
        grpc_server = container.order_grpc_server()
        tracing_service = container.tracing_service()
        asyncio.create_task(grpc_server.start_server())

        async with get_db() as session:
            pass
            # result = await session.execute(text("SELECT COUNT(*) FROM orders WHERE status = 'PENDING' OR status = 'COMPLETED'"))
            # count = result.scalar()
            # metrics_service.active_orders(count or 0)

        yield
        
        tracing_service.shutdown()

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

container.logging_service().initialize()
container.tracing_service().setup_tracing()
container.tracing_service().instrument_app(app=app)


# Prometheus metrics endpoint
metrics_service = container.metrics_service()

app.mount(
    "/metrics",
    make_asgi_app(registry=metrics_service.registry),
)

health_server = container.health_server() 

@app.get("/healthz")
async def health():
    return await health_server.health_check()


@app.get("/ready")
async def readiness(db: AsyncSession = Depends(database)):
    return await health_server.readiness_check(db)


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0",
                port=settings.HTTP_PORT, log_level=logging.INFO, reload=False)
