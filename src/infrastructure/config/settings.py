import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    GRPC_PORT: int = 50056
    API_PORT: int = 4004
    SERVICE_NAME: str = "OrderService"
    USER_SERVICE_NAME: str = "UserService"
    USER_SERVICE_GRPC: str = "user_srv:50052"
    USER_SERVICE_PORT: int = 50052
    
    COURSE_SERVICE_NAME: str = "CourseService"
    COURSE_SERVICE_GRPC: str = "course_srv:50053"
    COURSE_SERVICE_PORT: int = 50053
    
    SESSION_SERVICE_NAME: str = "SessionService"
    SESSION_SERVICE_GRPC: str = "localhost"
    SESSION_SERVICE_PORT: int = 50057
    
    DATABASE_URL_ASYNC: str = "postgresql+asyncpg://postgres:password@localhost:5433/order_service"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://postgres:password@localhost:5433/order_service"
    # DATABASE_URL: str = "postgresql+asyncpg://postgres:password@localhost:5433/order_service"
    
    KAFKA_BROKER: str = "kafka:29092"
    
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_TTL: int = 3600  # Cache TTL in seconds
    REDIS_KEY_PREFIX: str = "edulearn:order:"
    
    JAEGER_HOST: str = "localhost"
    JAEGER_PORT: int = 6831
    PROMETHEUS_PORT: int = 8000
    LOKI_URL: str = "http://localhost:3100"
    
    JWT_SECRET: str = "your-secret-key"
    
    MAX_CONNECTIONS: int = 100  # PostgreSQL connection pool max size
    KAFKA_CONSUMER_MAX_POLL_RECORDS: int = 100  # Batch size for Kafka consumer
    KAFKA_CONSUMER_GROUP: str = "order-service-group"

    model_config = SettingsConfigDict(
        env_file=".env" if os.getenv("DOCKER_ENV") != "true" else None,
        env_file_encoding="utf-8", extra="ignore")



@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Backward compatibility
settings = get_settings()


# from pydantic_settings import BaseSettings, SettingsConfigDict
# from typing import List, Optional
# from functools import lru_cache


# class DatabaseSettings(BaseSettings):
#     url: str = "postgresql+asyncpg://postgres:password@localhost:5432/order_service"
#     pool_size: int = 20
#     max_overflow: int = 30
#     pool_timeout: int = 30
#     pool_recycle: int = 3600
#     echo: bool = False
#     ssl_mode: str = "require"
#     ssl_ca_cert: Optional[str] = None
#     ssl_client_cert: Optional[str] = None
#     ssl_client_key: Optional[str] = None


# class KafkaSettings(BaseSettings):
#     brokers: List[str] = ["localhost:9092"]
#     consumer_group: str = "order-service-group"
#     consumer_max_poll_records: int = 100
#     producer_acks: str = "all"
#     producer_retries: int = 3
#     producer_batch_size: int = 16384
#     producer_linger_ms: int = 5
#     sasl_enabled: bool = False
#     sasl_mechanism: str = "PLAIN"
#     sasl_username: Optional[str] = None
#     sasl_password: Optional[str] = None
#     tls_enabled: bool = False
#     tls_ca_cert: Optional[str] = None
#     tls_client_cert: Optional[str] = None
#     tls_client_key: Optional[str] = None


# class RedisSettings(BaseSettings):
#     url: str = "redis://localhost:6379/0"
#     password: Optional[str] = None
#     db: int = 0
#     max_connections: int = 10
#     socket_timeout: int = 5
#     socket_connect_timeout: int = 5
#     retry_on_timeout: bool = True
#     health_check_interval: int = 30
#     ttl: int = 3600  # Default cache TTL in seconds


# class ObservabilitySettings(BaseSettings):
#     jaeger_host: str = "localhost"
#     jaeger_port: int = 6831
#     prometheus_port: int = 9090
#     loki_url: str = "http://localhost:3100"
#     log_level: str = "INFO"
#     log_format: str = "json"
#     metrics_enabled: bool = True
#     tracing_enabled: bool = True
#     logging_enabled: bool = True


# class SecuritySettings(BaseSettings):
#     jwt_secret: str = "your-secret-key-change-in-production"
#     jwt_algorithm: str = "HS256"
#     jwt_expiration_hours: int = 24
#     cors_origins: List[str] = ["*"]
#     cors_allow_credentials: bool = True
#     cors_allow_methods: List[str] = ["*"]
#     cors_allow_headers: List[str] = ["*"]


# class APISettings(BaseSettings):
#     port: int = 8000
#     host: str = "0.0.0.0"
#     workers: int = 1
#     reload: bool = False
#     access_log: bool = True
#     timeout_keep_alive: int = 5
#     timeout_graceful_shutdown: int = 30


# class GRPCSettings(BaseSettings):
#     port: int = 50051
#     host: str = "0.0.0.0"
#     max_concurrent_rpcs: int = 100
#     max_connection_idle: int = 300
#     max_connection_age: int = 600
#     max_connection_age_grace: int = 60
#     time: int = 7200
#     timeout: int = 20


# class OrderSettings(BaseSettings):
#     max_courses_per_order: int = 10
#     max_order_amount: float = 10000.0
#     order_expiration_minutes: int = 30
#     retry_attempts: int = 3
#     retry_backoff_multiplier: float = 2.0
#     retry_initial_delay: float = 1.0


# class Settings(BaseSettings):
#     # Environment
#     environment: str = "development"
#     debug: bool = False
    
#     # Service configuration
#     service_name: str = "order-service"
#     service_version: str = "1.0.0"
    
#     # Database
#     database: DatabaseSettings = DatabaseSettings()
    
#     # Kafka
#     kafka: KafkaSettings = KafkaSettings()
    
#     # Redis
#     redis: RedisSettings = RedisSettings()
    
#     # Observability
#     observability: ObservabilitySettings = ObservabilitySettings()
    
#     # Security
#     security: SecuritySettings = SecuritySettings()
    
#     # API
#     api: APISettings = APISettings()
    
#     # gRPC
#     grpc: GRPCSettings = GRPCSettings()
    
#     # Order-specific settings
#     order: OrderSettings = OrderSettings()

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         env_nested_delimiter="__",
#         case_sensitive=False,
#         extra="ignore"
#     )


# @lru_cache()
# def get_settings() -> Settings:
#     """Get cached settings instance."""
#     return Settings()


# # Backward compatibility
# settings = get_settings()