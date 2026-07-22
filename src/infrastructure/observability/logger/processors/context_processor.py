from structlog.types import EventDict

from .context import (
    correlation_id,
    trace_id,
    span_id,
    user_id,
)

class ContextProcessor:

    def __call__(self, logger, method_name, event_dict: EventDict):

        cid = correlation_id.get()

        if cid:
            event_dict["correlation_id"] = cid

        tid = trace_id.get()

        if tid:
            event_dict["trace_id"] = tid

        sid = span_id.get()

        if sid:
            event_dict["span_id"] = sid

        uid = user_id.get()

        if uid:
            event_dict["user_id"] = uid

        return event_dict