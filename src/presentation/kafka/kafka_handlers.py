from src.application.use_cases.order.interfaces.order_failed_usecase_interface import IOrderFailedUseCase
from src.application.use_cases.order.interfaces.order_payment_initiated_usecase_interface import IOrderPaymentInitiatedUseCase
from src.application.use_cases.order.interfaces.order_success_usecase_interface import IOrderSuccessUseCase
from src.application.use_cases.order.interfaces.order_timeout_usecase_interface import IOrderTimeoutUseCase
from src.domain.events.order_payment_timeout_event import OrderPaymentTimeoutEventDto
from src.domain.events.order_payment_initiate_event import OrderPaymentInitiatedEventDto
from src.domain.events.order_payment_failure_event import OrderPaymentFailureEventDto
from src.domain.events.order_payment_success_event import OrderPaymentSuccessEventDto

from src.shared.events.topics import EVENT_TOPICS
from src.infrastructure.kafka.handler_registry import (
    KafkaHandlerRegistryMixin,
    kafka_handler,
)


class KafkaEventHandlers(KafkaHandlerRegistryMixin):
    def __init__(
        self,
        payment_initiated_handler: IOrderPaymentInitiatedUseCase,
        order_success_handler: IOrderSuccessUseCase,
        order_failed_handler: IOrderFailedUseCase,
        order_timeout_handler: IOrderTimeoutUseCase,
    ):
        # Dependencies must be assigned before super().__init__(), since
        # registration binds handler methods to `self`.
        self.payment_initiated_handler = payment_initiated_handler
        self.order_success_handler = order_success_handler
        self.order_timeout_handler = order_timeout_handler
        self.order_failed_handler = order_failed_handler

        super().__init__()  # builds self._topic_handlers from @kafka_handler tags

    @kafka_handler(EVENT_TOPICS.PAYMENT_ORDER_INITIATED.value)
    async def handle_payment_created(self, event: dict) -> None:
        dto = OrderPaymentInitiatedEventDto.from_payload(event=event)
        await self.payment_initiated_handler.execute(dto)

    @kafka_handler(EVENT_TOPICS.PAYMENT_ORDER_SUCCEEDED.value)
    async def handle_payment_succeed(self, event: dict) -> None:
        dto = OrderPaymentSuccessEventDto.from_payload(event=event)
        await self.order_success_handler.execute(dto)

    @kafka_handler(EVENT_TOPICS.PAYMENT_ORDER_FAILED.value)
    async def handle_payment_failed(self, event: dict) -> None:
        dto = OrderPaymentFailureEventDto.from_payload(event=event)
        await self.order_failed_handler.execute(dto)

    @kafka_handler(EVENT_TOPICS.PAYMENT_ORDER_TIMEOUT.value)
    async def handle_payment_timeout(self, event: dict) -> None:
        dto = OrderPaymentTimeoutEventDto.from_payload(event=event)
        await self.order_timeout_handler.execute(dto)