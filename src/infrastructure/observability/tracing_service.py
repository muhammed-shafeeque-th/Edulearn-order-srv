from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from src.application.interfaces.tracing_interface import ITracingService
from src.infrastructure.config.settings import settings


class TracingService(ITracingService):
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TracingService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        if not self._initialized:
            self._tracer_provider: None | TracerProvider = None
            self._initialized = True

    def setup_tracing(self) -> None:
        if self._tracer_provider is None:
            # Check if a tracer provider already exists
            current_provider = trace.get_tracer_provider()
            if isinstance(current_provider, TracerProvider):
                # A tracer provider already exists, use it
                self._tracer_provider = current_provider
            else:
                # Create a new tracer provider
                resource = Resource(attributes={SERVICE_NAME: "order-service"})
                self._tracer_provider = TracerProvider(resource=resource)
                trace.set_tracer_provider(self._tracer_provider)

                jaeger_exporter = JaegerExporter(
                    agent_host_name=settings.JAEGER_HOST,
                    agent_port=settings.JAEGER_PORT
                )

                span_processor = BatchSpanProcessor(jaeger_exporter)
                self._tracer_provider.add_span_processor(
                    span_processor=span_processor)

    def instrument_app(self, app: FastAPI):
        FastAPIInstrumentor.instrument_app(app)

    def get_tracer(self) -> trace.Tracer:
        return trace.get_tracer(settings.SERVICE_NAME)
