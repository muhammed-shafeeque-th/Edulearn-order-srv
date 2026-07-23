
from dataclasses import dataclass
from logging import INFO


@dataclass(slots=True)
class LoggerConfig:
    service_name: str
    environment: str = "development"
    version: str = "1.0.0"

    level: int = INFO

    json_logs: bool = False
    pretty_logs: bool = True

    include_callsite: bool = True
    include_stack_info: bool = False