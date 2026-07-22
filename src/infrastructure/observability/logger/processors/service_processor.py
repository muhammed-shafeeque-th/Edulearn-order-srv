import os
import socket

from structlog.types import EventDict


class ServiceContextProcessor:

    def __init__(
        self,
        service_name: str,
        environment: str,
        version: str,
    ):
        self.service_name = service_name
        self.environment = environment
        self.version = version

        self.hostname = socket.gethostname()
        self.pid = os.getpid()

    def __call__(
        self,
        logger,
        method_name,
        event_dict: EventDict,
    ) -> EventDict:

        event_dict.setdefault("service.name", self.service_name)
        event_dict.setdefault("service.version", self.version)
        event_dict.setdefault(
            "deployment.environment",
            self.environment,
        )

        event_dict.setdefault(
            "host.name",
            self.hostname,
        )

        event_dict.setdefault(
            "process.pid",
            self.pid,
        )

        return event_dict