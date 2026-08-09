
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.redis_interface import IRedisService
from src.infrastructure.kafka.consumer import KafkaConsumer
from src.infrastructure.database.database import db, AsyncSession
from fastapi import  Depends, HTTPException
from sqlalchemy import text




class HealthServer:
    def __init__(self, logger: ILoggingService, redis: IRedisService,  kafka: KafkaConsumer) -> None:
        self.logger = logger.get_logger("HealthServer")
        self.kafka = kafka
        self.redis = redis
        
    
    async def health_check(self):
        try:
            return {"status": "healthy"}
        except Exception as e:
            self.logger.error(
                f"Health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail="Service Unhealthy")
    
    async def readiness_check(self, db: AsyncSession):
        status = {
            "redis": "up",
            "database": "up",
            "kafka": "up",
        }
        try:
            try:
                await db.execute(text("SELECT 1"))
            except Exception as e:
                status["database"] = "down"
                raise
            
            try:  
                await self.redis.client.ping()
            except Exception as e:
                status["redis"] = "down"
                raise
            
            kafka_is_healthy = await self.kafka.is_healthy()
            status["kafka"] = "up" if kafka_is_healthy else "down"
            
            is_all_healthy = all(value == "up" for value in status.values())
            if not is_all_healthy:
                raise RuntimeError("One or more readiness checks failed")
            
            return {"status": "healthy", **status}
        except Exception as e:
            self.logger.error(f"Health check failed: {str(e)}")
            raise HTTPException(status_code=503, detail={"status": "unhealthy", **status})
