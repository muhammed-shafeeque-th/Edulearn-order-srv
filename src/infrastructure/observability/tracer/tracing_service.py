from __future__ import annotations

from fastapi import FastAPI

from opentelemetry import trace
from opentelemetry.trace import Tracer

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.sdk.resources import DEPLOYMENT_ENVIRONMENT

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
# from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

from src.application.interfaces.tracing_interface import ITracingService
from src.infrastructure.config.settings import settings


class TracingService(ITracingService):
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._provider: TracerProvider | None = None
        self._initialized = True

    def setup_tracing(self) -> None:

        if self._provider is not None:
            return

        provider = trace.get_tracer_provider()

        if isinstance(provider, TracerProvider):
            self._provider = provider
            return

        resource = Resource.create(
            {
                SERVICE_NAME: settings.SERVICE_NAME,
                DEPLOYMENT_ENVIRONMENT: settings.ENVIRONMENT,
                "service.version": settings.APP_VERSION,
            }
        )

        self._provider = TracerProvider(resource=resource)

        exporter = OTLPSpanExporter(
            endpoint=settings.OTLP_ENDPOINT,
            # insecure=settings.OTEL_EXPORTER_OTLP_INSECURE,
        )

        processor = BatchSpanProcessor(
            exporter,
            max_queue_size=2048,
            max_export_batch_size=512,
            schedule_delay_millis=5000,
            export_timeout_millis=30000,
        )

        self._provider.add_span_processor(processor)

        trace.set_tracer_provider(self._provider)

    def instrument_app(self, app: FastAPI):

        FastAPIInstrumentor.instrument_app(
            app,
            tracer_provider=self._provider,
        )
        RequestsInstrumentor().instrument()

        RedisInstrumentor().instrument()

        # Psycopg2Instrumentor().instrument()

    def get_tracer(self, name: str | None = None) -> Tracer:

        return trace.get_tracer(
            name or settings.SERVICE_NAME,
            settings.APP_VERSION,
        )

    def shutdown(self):

        if self._provider:
            self._provider.shutdown()
