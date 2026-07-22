from contextvars import ContextVar

correlation_id = ContextVar("correlation_id", default=None)
trace_id = ContextVar("trace_id", default=None)
span_id = ContextVar("span_id", default=None)
user_id = ContextVar("user_id", default=None)


def bind_context(
    *,
    correlation=None,
    trace=None,
    span=None,
    user=None,
):
    if correlation is not None:
        correlation_id.set(correlation)

    if trace is not None:
        trace_id.set(trace)

    if span is not None:
        span_id.set(span)

    if user is not None:
        user_id.set(user)


def clear_context():
    correlation_id.set(None)
    trace_id.set(None)
    span_id.set(None)
    user_id.set(None)