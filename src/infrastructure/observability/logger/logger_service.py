from __future__ import annotations

import logging
from typing import Any, Optional

from structlog.stdlib import BoundLogger

from src.infrastructure.observability.logger.logger_manager import LoggerManager
from src.application.interfaces.logging_interface import ILoggingService

from .processors.context import (
    bind_context,
    clear_context,
    # unbind_context,
)


class LoggingService(ILoggingService):
    """
    Thin wrapper around structlog.
    
    """

    def __init__(
        self,
        logger_manager: LoggerManager,
    ) -> None:
        self._manager = logger_manager
       
        self._logger: BoundLogger 
        self._level = logging.INFO

    # Lifecycle

    def initialize(self):
        self._manager.initialize()

        self._logger = self._manager.get_logger()
        self._logger.info(
                "Logger initialized",
            )
        return

    def shutdown(self) -> None:
        """
        Flush stdlib handlers.
        """

        logging.shutdown()

    # Logger Access

    def get_logger(
        self,
        name: Optional[str] = None,
    ) -> BoundLogger:

        if name:
            return self._logger.bind(component=name)

        return self._logger

    def child(self, **context):

        service = LoggingService(self._manager)

        service._logger = self._logger.bind(**context)

        return service
    # Context

    def bind(
        self,
        **context: Any,
    ) -> None:

        bind_context(**context)

    def unbind(
        self,
        *keys: str,
    ) -> None:

        clear_context(*keys)

    def clear(self) -> None:

        clear_context()

    # Log methods

    def debug(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self._logger.debug(message, **kwargs)

    def info(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self._logger.info(message, **kwargs)

    def warning(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self._logger.warning(message, **kwargs)

    def warn(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self.warning(message, **kwargs)

    def error(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self._logger.error(message, **kwargs)

    def critical(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self._logger.critical(message, **kwargs)

    def exception(
        self,
        message: str,
        **kwargs: Any,
    ) -> None:

        self._logger.exception(message, **kwargs)

    # Helpers

    def is_enabled_for(
        self,
        level: int,
    ) -> bool:

        return logging.getLogger().isEnabledFor(level)

    def set_level(
        self,
        level: int,
    ) -> None:

        logging.getLogger().setLevel(level)
        self._level = level

    @property
    def level(self) -> int:
        return self._level
    