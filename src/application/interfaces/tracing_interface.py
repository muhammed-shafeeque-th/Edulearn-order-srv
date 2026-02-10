from abc import ABC, abstractmethod
from opentelemetry import trace
from fastapi import FastAPI


class ITracingService(ABC):
    @abstractmethod
    def setup_tracing(self) -> None:
        pass

    @abstractmethod
    def instrument_app(self, app: "FastAPI") -> None:
        pass

    @abstractmethod
    def get_tracer(self) -> "trace.Tracer":
        pass
