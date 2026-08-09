
from __future__ import annotations

import inspect
from typing import Any, Awaitable, Callable

HandlerFunc = Callable[..., Awaitable[None]]


class UnknownTopicError(Exception):
    """Raised when dispatch() is called for a topic with no registered handler.

    Consider moving this into src/domain/exceptions/exceptions.py to keep
    it consistent with the rest of your exception hierarchy.
    """

    def __init__(self, topic: str):
        super().__init__(f"No handler registered for topic: {topic}")
        self.topic = topic


class DuplicateHandlerError(Exception):
    """Raised at startup if two handlers claim the same topic."""

    def __init__(self, topic: str, existing: str, new: str):
        super().__init__(
            f"Duplicate handler registration for topic '{topic}': "
            f"'{existing}' and '{new}' both claim it."
        )


def kafka_handler(*topics: str) -> Callable[[HandlerFunc], HandlerFunc]:
    """Mark a coroutine method as the handler for one or more Kafka topics.

    Can be stacked / called with multiple topics if one handler legitimately
    services more than one topic:

        @kafka_handler(TOPIC_A, TOPIC_B)
        async def handle_both(self, event: dict) -> None: ...
    """
    if not topics:
        raise ValueError("kafka_handler() requires at least one topic")

    def decorator(func: HandlerFunc) -> HandlerFunc:
        if not inspect.iscoroutinefunction(func):
            raise TypeError(
                f"@kafka_handler can only decorate async def methods, "
                f"got '{func.__name__}'"
            )
        existing = getattr(func, "_kafka_topics", [])
        func._kafka_topics = [*existing, *topics]  # type: ignore[attr-defined]
        return func

    return decorator


class KafkaHandlerRegistryMixin:
    """Scans the subclass for @kafka_handler-decorated methods and builds
    a topic -> bound-handler dispatch table.

    Subclasses MUST call `super().__init__()` after their own dependencies
    are assigned to `self`, since handlers are bound (and may close over
    `self`'s attributes) at registration time.
    """

    def __init__(self) -> None:
        self._topic_handlers: dict[str, HandlerFunc] = {}
        self._register_handlers()

    def _register_handlers(self) -> None:
        for attr_name in dir(type(self)):
            attr = getattr(type(self), attr_name, None)
            topics = getattr(attr, "_kafka_topics", None)
            if not topics:
                continue

            bound_handler: HandlerFunc = getattr(self, attr_name)
            for topic in topics:
                if topic in self._topic_handlers:
                    raise DuplicateHandlerError(
                        topic=topic,
                        existing=self._topic_handlers[topic].__name__,
                        new=bound_handler.__name__,
                    )
                self._topic_handlers[topic] = bound_handler

    async def dispatch(self, topic: str, event: dict[str, Any]) -> None:
        """Invoke the handler registered for `topic`.

        Raises UnknownTopicError if nothing is registered for it.
        """
        handler = self._topic_handlers.get(topic)
        if handler is None:
            raise UnknownTopicError(topic)
        await handler(event=event)

    def has_handler(self, topic: str) -> bool:
        return topic in self._topic_handlers

    def get_registered_topics(self) -> list[str]:
        return list(self._topic_handlers.keys())