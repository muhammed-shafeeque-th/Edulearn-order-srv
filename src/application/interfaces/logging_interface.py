from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import structlog

class ILoggingService(ABC):
    @abstractmethod
    def get_logger(self, name: str) -> "structlog.stdlib.BoundLogger":
        pass
    
    # @abstractmethod
    # def initialize(self) -> "structlog.stdlib.BoundLogger":
    #     pass
    
    @abstractmethod
    def bind(self, **kwargs: Any) -> None:
        pass
    
    @abstractmethod
    def unbind(self, *keys: str) -> None:
        pass