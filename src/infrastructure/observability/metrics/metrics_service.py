import threading

from src.application.interfaces.metrics_interface import IMetricsService
import threading

from prometheus_client import (
    CollectorRegistry,
    Counter,
    Gauge,
    Histogram,
    ProcessCollector,
    PlatformCollector,
    GCCollector,
)


class MetricsService(IMetricsService):
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized"):
            return

        self.registry = CollectorRegistry()

        # Default runtime metrics
        ProcessCollector(registry=self.registry)
        PlatformCollector(registry=self.registry)
        GCCollector(registry=self.registry)

        self._request_counter = Counter(
            "order_service_requests_total",
            "Total number of requests",
            ["method", "endpoint", "status"],
            registry=self.registry,
        )

        self._request_latency = Histogram(
            "order_service_request_latency_seconds",
            "HTTP request latency",
            ["method", "endpoint"],
            buckets=(
                0.001,
                0.005,
                0.01,
                0.025,
                0.05,
                0.1,
                0.25,
                0.5,
                1,
                2,
                5,
            ),
            registry=self.registry,
        )

        self._active_orders = Gauge(
            "order_service_active_orders",
            "Number of active orders",
            registry=self.registry,
        )

        self._cache_hits = Counter(
            "order_service_cache_hits_total",
            "Total cache hits",
            ["type"],
            registry=self.registry,
        )

        self._cache_misses = Counter(
            "order_service_cache_misses_total",
            "Total cache misses",
            ["type"],
            registry=self.registry,
        )

        self._saga_failures = Counter(
            "order_service_saga_failures_total",
            "Total SAGA failures",
            ["step"],
            registry=self.registry,
        )

        self._initialized = True

    def setup_metrics(self) -> None:
        """
        Initializes the metrics registry.

        Metrics are created during service initialization.
        """
        return

    def request_counter(self, method: str, endpoint: str, status: str) -> None:
        self._request_counter.labels(
            method=method, endpoint=endpoint, status=status).inc()

    def request_latency(self, method: str, endpoint: str, latency: float) -> None:
        self._request_latency.labels(
            method=method, endpoint=endpoint).observe(latency)

    def active_orders(self, count: int) -> None:
        self._active_orders.set(count)

    def cache_hits(self, type: str) -> None:
        self._cache_hits.labels(type=type).inc()

    def cache_misses(self, type: str) -> None:
        self._cache_misses.labels(type=type).inc()

    def saga_failures(self, step: str) -> None:
        self._saga_failures.labels(step=step).inc()
