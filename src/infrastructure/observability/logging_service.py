import json
import logging
import sys
import time
import threading
from typing import Any, Dict, Optional, List
from contextlib import contextmanager
from functools import wraps
import requests
import structlog
from structlog.stdlib import LoggerFactory
from structlog.processors import (
    TimeStamper,
    JSONRenderer,
    add_log_level,
    StackInfoRenderer,
    format_exc_info,
    UnicodeDecoder,
    CallsiteParameterAdder,
)
from structlog.types import Processor, EventDict

from src.application.interfaces.logging_interface import ILoggingService
from src.infrastructure.config.settings import settings


class AsyncLokiHandler(logging.Handler):
    """Asynchronous Loki handler with batching and retry logic."""

    def __init__(self, loki_url: str, batch_size: int = 100, flush_interval: float = 5.0):
        super().__init__()
        self.loki_url = loki_url
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.batch: List[Dict[str, Any]] = []
        self._batch_lock: threading.Lock = threading.Lock()
        self.last_flush = time.time()
        self._shutdown = False

        # Start background flush thread
        self.flush_thread = threading.Thread(
            target=self._flush_worker, daemon=True)
        self.flush_thread.start()

    def emit(self, record: logging.LogRecord) -> None:
        """Emit a log record to the batch."""
        if self._shutdown:
            return

        try:
            log_entry = self.format(record)
            log_data = {
                "streams": [
                    {
                        "stream": {
                            "service": settings.SERVICE_NAME,
                            "level": record.levelname.lower(),
                            "logger": record.name,
                            "module": record.module,
                            "function": record.funcName,
                        },
                        "values": [[str(int(record.created * 1e9)), log_entry]],
                    }
                ]
            }

            with self._batch_lock:
                self.batch.append(log_data)

                # Flush if batch is full or enough time has passed
                current_time = time.time()
                if (len(self.batch) >= self.batch_size or
                        current_time - self.last_flush >= self.flush_interval):
                    self._flush_batch()

        except Exception as e:
            # Fallback to stderr to avoid infinite loops
            sys.stderr.write(f"Failed to emit log to Loki: {e}\n")

    def _flush_batch(self) -> None:
        """Flush the current batch to Loki."""
        if not self.batch:
            return

        batch_to_send = self.batch.copy()
        self.batch.clear()
        self.last_flush = time.time()

        # Send batch asynchronously
        threading.Thread(target=self._send_batch, args=(
            batch_to_send,), daemon=True).start()

    def _send_batch(self, batch: List[Dict[str, Any]]) -> None:
        """Send a batch of logs to Loki with retry logic."""
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                # Combine all streams from the batch
                combined_streams = []
                for log_data in batch:
                    combined_streams.extend(log_data["streams"])

                payload = {"streams": combined_streams}

                response = requests.post(
                    url=f"{self.loki_url}/loki/api/v1/push",
                    headers={"Content-Type": "application/json"},
                    data=json.dumps(payload),
                    timeout=10,
                )

                if response.status_code < 300:
                    return
                else:
                    sys.stderr.write(
                        f"Loki logging failed: {response.status_code} - {response.text}\n"
                    )

            except Exception as e:
                sys.stderr.write(
                    f"Failed to send batch to Loki (attempt {attempt + 1}): {e}\n")

            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff

    def _flush_worker(self) -> None:
        """Background worker to periodically flush logs."""
        while not self._shutdown:
            time.sleep(self.flush_interval)
            with self._batch_lock:
                if self.batch:
                    self._flush_batch()

    def close(self) -> None:
        """Close the handler and flush remaining logs."""
        self._shutdown = True
        with self._batch_lock:
            if self.batch:
                self._flush_batch()
        super().close()


class ColorfulLogLevelProcessor:
    """Processor to add colorful log levels."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def __call__(self, logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        """Add colorful log level to the event."""
        level = event_dict.get('level', 'INFO').upper()
        color = self.COLORS.get(level, self.COLORS['RESET'])
        # event_dict['level_color'] = f"{color}{level}{self.COLORS['RESET']}"
        return event_dict


class CallerLocationProcessor:
    """Processor to add caller location information."""
    
    def __call__(self, logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        """Add caller location information to the event."""
        import inspect
        
        # Get the caller frame (skip this processor and the logging call)
        frame = inspect.currentframe()
        caller_frame = None
        
        # Walk up the stack to find the actual caller
        for _ in range(10):  # Limit to prevent infinite loops
            if frame is None:
                break
            frame = frame.f_back
            if frame is None:
                break
                
            # Skip internal logging frames
            filename = frame.f_code.co_filename
            if ('structlog' not in filename and 
                'logging' not in filename and 
                'observability' not in filename):
                caller_frame = frame
                break
        
        if caller_frame:
            module = inspect.getmodule(caller_frame)
            module_name = module.__name__ if module else 'unknown'
            event_dict.update({
                # 'caller_file': caller_frame.f_code.co_filename,
                # 'caller_function': caller_frame.f_code.co_name,
                # 'caller_line': caller_frame.f_lineno,
                # 'caller_module': module_name
                'caller': f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"
            })
        
        return event_dict


class PerformanceProcessor:
    """Processor to add performance metrics to logs."""

    def __init__(self):
        self.start_times: Dict[int, float] = {}

    def __call__(self, logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        """Add performance metrics to the log event."""
        thread_id = threading.get_ident()

        if method_name == "performance_start":
            self.start_times[thread_id] = time.time()
            event_dict["event"] = "performance_start"
            return event_dict
        elif method_name == "performance_end":
            start_time = self.start_times.pop(thread_id, None)
            if start_time:
                duration = time.time() - start_time
                event_dict["duration_ms"] = round(duration * 1000, 2)
                event_dict["event"] = "performance_end"
            return event_dict

        return event_dict


class CorrelationProcessor:
    """Processor to add correlation IDs to logs."""

    def __init__(self):
        self.correlation_id = threading.local()

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set correlation ID for current thread."""
        self.correlation_id.value = correlation_id

    def get_correlation_id(self) -> Optional[str]:
        """Get correlation ID for current thread."""
        return getattr(self.correlation_id, 'value', None)

    def __call__(self, logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        """Add correlation ID to the log event."""
        correlation_id = self.get_correlation_id()
        if correlation_id:
            event_dict["correlation_id"] = correlation_id
        return event_dict


class ConsoleFormatter(logging.Formatter):
    """Custom console formatter for colorful and readable logs."""
    
    def __init__(self, use_colors: bool = True):
        super().__init__()
        self.use_colors = use_colors
        self.colors = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',    # Red
            'CRITICAL': '\033[35m', # Magenta
            'RESET': '\033[0m'      # Reset
        }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors and caller information."""
        # Get the log level
        level = record.levelname
        
        # Get caller information from the record
        # caller_file = getattr(record, 'caller_file', 'unknown')
        # caller_function = getattr(record, 'caller_function', 'unknown')
        # caller_line = getattr(record, 'caller_line', 0)
        caller = getattr(record, 'caller', "unknown")
        # caller_module = getattr(record, 'caller_module', 'unknown')
        # Format timestamp
        timestamp = record.created
        
        # Format the message
        if self.use_colors:
            color = self.colors.get(level, self.colors['RESET'])
            reset = self.colors['RESET']
            formatted = (
                f"{color}[{level}]{reset} "
                # f"{timestamp} "
                # f"{color}{caller_module}:{caller_function}:{caller_line}{reset} "
                f"{record.getMessage()}"
            )
        else:
            formatted = (
                f"[{level}] "
                # f"{timestamp} "
                # f"{caller_module}:{caller_file}:{caller_line} "
                f"{caller} "
                f"{record.getMessage()}"
            )
        
        return formatted


class LoggingService(ILoggingService):
    """Enhanced logging service using structlog with best practices."""

    _instance: Optional['LoggingService'] = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls) -> 'LoggingService':
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LoggingService, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not self._initialized:
            self._logger: Optional[structlog.stdlib.BoundLogger] = None
            self._correlation_processor = CorrelationProcessor()
            self._performance_processor = PerformanceProcessor()
            self._colorful_level_processor = ColorfulLogLevelProcessor()
            self._caller_location_processor = CallerLocationProcessor()
            self._context: Dict[str, Any] = {}
            self._initialized = True

    def setup_logger(self) -> structlog.stdlib.BoundLogger:
        """Setup and configure structlog with all processors and handlers."""
        if self._logger is None:
            # Configure structlog
            structlog.configure(
                processors=[
                    # Add timestamp
                    TimeStamper(fmt="iso"),

                    # Add log level
                    add_log_level,

                    # Add colorful log levels
                    self._colorful_level_processor,

                    # Add caller location
                    self._caller_location_processor,

                    # Add stack info
                    StackInfoRenderer(),

                    # Add exception info
                    format_exc_info,

                    # Add performance metrics
                    self._performance_processor,

                    # Add correlation ID
                    self._correlation_processor,

                    # Add service context
                    self._add_service_context,

                    # Render as JSON
                    JSONRenderer(),
                ],
                wrapper_class=structlog.stdlib.BoundLogger,
                logger_factory=LoggerFactory(),
                cache_logger_on_first_use=True,
            )

            # Configure standard library logging with custom formatter
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(ConsoleFormatter(use_colors=True))
            
            # Configure root logger
            root_logger = logging.getLogger()
            root_logger.setLevel(logging.INFO)
            root_logger.addHandler(console_handler)

            # Add Loki handler
            root_logger = logging.getLogger()
            loki_handler = AsyncLokiHandler(
                loki_url=settings.LOKI_URL,
                batch_size=50,  # Smaller batch for faster delivery
                flush_interval=2.0,  # More frequent flushing
            )
            root_logger.addHandler(loki_handler)

            # Create the main logger
            self._logger = structlog.get_logger(settings.SERVICE_NAME)

        assert self._logger is not None
        return self._logger

    def _add_service_context(self, logger: Any, method_name: str, event_dict: EventDict) -> EventDict:
        """Add service-specific context to all log events."""
        event_dict.update({
            "service": settings.SERVICE_NAME,
            "environment": getattr(settings, 'ENVIRONMENT', 'development'),
            **self._context,
        })
        return event_dict

    def get_logger(self, name: str) -> structlog.stdlib.BoundLogger:
        """Get a logger with the specified name."""
        if not self._logger:
            self.setup_logger()

        assert self._logger is not None
        return self._logger.bind(logger_name=name)

    def bind_context(self, **kwargs: Any) -> structlog.stdlib.BoundLogger:
        """Bind context variables to all subsequent log events."""
        if not self._logger:
            self.setup_logger()

        self._context.update(kwargs)
        assert self._logger is not None
        return self._logger.bind(**kwargs)

    def unbind_context(self, *keys: str) -> structlog.stdlib.BoundLogger:
        """Unbind context variables from all subsequent log events."""
        if not self._logger:
            self.setup_logger()

        for key in keys:
            self._context.pop(key, None)

        assert self._logger is not None
        return self._logger

    def set_correlation_id(self, correlation_id: str) -> None:
        """Set correlation ID for the current thread."""
        self._correlation_processor.set_correlation_id(correlation_id)

    def get_correlation_id(self) -> Optional[str]:
        """Get correlation ID for the current thread."""
        return self._correlation_processor.get_correlation_id()

    @contextmanager
    def performance_tracking(self, operation: str, **context: Any):
        """Context manager for tracking performance of operations."""
        if not self._logger:
            self.setup_logger()

        assert self._logger is not None
        logger = self._logger.bind(operation=operation, **context)
        logger.performance_start()  # type: ignore

        try:
            yield logger
        finally:
            logger.performance_end()  # type: ignore

    def log_exception(self, exception: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """Log an exception with full context."""
        if not self._logger:
            self.setup_logger()

        assert self._logger is not None
        logger = self._logger
        if context:
            logger = logger.bind(**context)

        logger.error(
            "Exception occurred",
            exc_info=True,
            exception_type=type(exception).__name__,
            exception_message=str(exception),
        )

    def log_request(self, method: str, url: str, status_code: int, duration: float, **context: Any) -> None:
        """Log HTTP request details."""
        if not self._logger:
            self.setup_logger()

        assert self._logger is not None
        self._logger.info(
            "HTTP request",
            method=method,
            url=url,
            status_code=status_code,
            duration_ms=round(duration * 1000, 2),
            **context,
        )

    def log_database_query(self, query: str, duration: float, **context: Any) -> None:
        """Log database query details."""
        if not self._logger:
            self.setup_logger()

        assert self._logger is not None
        self._logger.debug(
            "Database query",
            query=query,
            duration_ms=round(duration * 1000, 2),
            **context,
        )


def log_performance(operation: str):
    """Decorator to automatically log performance of functions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggingService()
            with logger.performance_tracking(operation, function=func.__name__):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def log_exceptions(context: Optional[Dict[str, Any]] = None):
    """Decorator to automatically log exceptions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger = LoggingService()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log_exception(e, context)
                raise
        return wrapper
    return decorator
