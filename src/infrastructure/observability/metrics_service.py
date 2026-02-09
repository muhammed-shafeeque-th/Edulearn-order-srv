import threading
from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, REGISTRY

from src.application.interfaces.metrics_interface import IMetricsService

class MetricsService(IMetricsService):
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(MetricsService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self._request_counter = Counter("order_service_requests_total", "Total number of requests", ["method", "endpoint", "status"])
        self._request_latency = Histogram("order_service_request_latency_seconds", "Request latency in seconds", ["method", "endpoint"])
        self._active_orders = Gauge("order_service_active_orders", "Number of active orders")
        self._cache_hits = Counter("order_service_cache_hits_total", "Total cache hits", ["type"])
        self._cache_misses = Counter("order_service_cache_misses_total", "Total cache misses", ["type"])
        self._saga_failures = Counter("order_service_saga_failures_total", "Total SAGA failures", ["step"])

    def setup_metrics(self) -> None:
        # Metrics are already initialized in constructor, no need to do anything here
        pass

    def request_counter(self, method: str, endpoint: str, status: str) -> None:
        self._request_counter.labels(method=method, endpoint=endpoint, status=status).inc()

    def request_latency(self, method: str, endpoint: str, latency: float) -> None:
        self._request_latency.labels(method=method, endpoint=endpoint).observe(latency)

    def active_orders(self, count: int) -> None:
        self._active_orders.set(count)

    def cache_hits(self, type: str) -> None:
        self._cache_hits.labels(type=type).inc()

    def cache_misses(self, type: str) -> None:
        self._cache_misses.labels(type=type).inc()

    def saga_failures(self, step: str) -> None:
        self._saga_failures.labels(step=step).inc()