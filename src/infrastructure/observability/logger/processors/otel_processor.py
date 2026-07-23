from opentelemetry.trace import get_current_span
from structlog.types import EventDict


class OpenTelemetryProcessor:

    def __call__(
        self,
        logger,
        method_name,
        event_dict: EventDict,
    ) -> EventDict:

        span = get_current_span()

        if not span:
            return event_dict

        ctx = span.get_span_context()

        if not ctx.is_valid:
            return event_dict

        event_dict["trace_id"] = format(
            ctx.trace_id,
            "032x",
        )

        event_dict["span_id"] = format(
            ctx.span_id,
            "016x",
        )

        return event_dict