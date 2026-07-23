from __future__ import annotations

import logging
import sys
from threading import Lock

import structlog

from structlog.stdlib import LoggerFactory
from structlog.stdlib import BoundLogger

from .logger_config import LoggerConfig
from .processors import *


from structlog.dev import ConsoleRenderer
from structlog.processors import (
    JSONRenderer,
    TimeStamper,
    StackInfoRenderer,
    format_exc_info,
    UnicodeDecoder,
    add_log_level,
)
from structlog.processors import (
    CallsiteParameterAdder,
    CallsiteParameter,
)

from structlog.stdlib import LoggerFactory

from structlog.contextvars import merge_contextvars



class LoggerManager:

    _instance: "LoggerManager | None" = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config: LoggerConfig, ):

        if hasattr(self, "_initialized"):
            return

        self._initialized = True
        self._configured = False
        
        self._config = config

        self._logger: BoundLogger | None = None
        # Use the interface type so return types match ILoggingService
        # self._service: ILoggingService | None = None

    def initialize(
        self,
    ) -> BoundLogger:

        if self._configured:
            # _service must be set if configured
            assert self._logger is not None
            return self._logger

        renderer = (
            JSONRenderer()
            if self._config.json_logs
            else ConsoleRenderer()
        )

        logging.basicConfig(
            stream=sys.stdout,
            level=self._config.level,
            format="%(message)s",
            force=True,
        )

        processors = [

            context_processor.ContextProcessor(),

            otel_processor.OpenTelemetryProcessor(),

            service_processor.ServiceContextProcessor(
                self._config.service_name,
                self._config.environment,
                self._config.version,
            ),


            structlog.stdlib.add_log_level,

            merge_contextvars,


            TimeStamper(fmt="iso"),


            UnicodeDecoder(),

        ]

        if self._config.include_callsite:

            processors.append(

                CallsiteParameterAdder(
                    {
                        CallsiteParameter.MODULE,
                        CallsiteParameter.FILENAME,
                        CallsiteParameter.FUNC_NAME,
                        CallsiteParameter.LINENO,
                    }
                )
            )

        processors.extend(

            [

                StackInfoRenderer(),

                format_exc_info,

                renderer,

            ]

        )

        structlog.configure(

            processors=processors,

            wrapper_class=structlog.make_filtering_bound_logger(
                self._config.level
            ),

            logger_factory=LoggerFactory(),

            cache_logger_on_first_use=True,

        )

        self._logger = structlog.get_logger(self._config.service_name)
        
        assert self._logger is not None
            
        self._configured = True
            
       

        return self._logger

    def get_logger(self) -> BoundLogger:

        if self._logger is None:
            raise RuntimeError(
                "LoggerManager.initialize() has not been called."
            )

        return self._logger

    def shutdown(self):

        logging.shutdown()

        self._configured = False
