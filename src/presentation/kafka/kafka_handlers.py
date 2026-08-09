from src.application.use_cases.order.interfaces.order_failed_usecase_interface import IOrderFailedUseCase
from src.application.use_cases.order.interfaces.order_payment_initiated_usecase_interface import IOrderPaymentInitiatedUseCase
from src.application.use_cases.order.interfaces.order_success_usecase_interface import IOrderSuccessUseCase
from src.application.use_cases.order.interfaces.order_timeout_usecase_interface import IOrderTimeoutUseCase
from src.domain.events.order_payment_timeout_event import OrderPaymentTimeoutEventDto

from src.domain.events.order_payment_initiate_event import OrderPaymentInitiatedEventDto
from src.domain.events.order_payment_failure_event import OrderPaymentFailureEventDto
from src.domain.events.order_payment_success_event import OrderPaymentSuccessEventDto


class KafkaEventHandlers:
    def __init__(
        self,
        payment_initiated_handler: IOrderPaymentInitiatedUseCase,
        order_success_handler:  IOrderSuccessUseCase,
        order_failed_handler: IOrderFailedUseCase,
        order_timeout_handler: IOrderTimeoutUseCase,
    ):

        
        self.payment_initiated_handler = payment_initiated_handler
        self.order_success_handler = order_success_handler
        self.order_timeout_handler = order_timeout_handler
        self.order_failed_handler = order_failed_handler
       

    async def handle_payment_created(self,  event: dict) -> None:
        dto = OrderPaymentInitiatedEventDto.from_payload(
                            event=event,
                        )
        await self.payment_initiated_handler.execute(dto)
        
        
        
    async def handle_payment_succeed(self,  event: dict) -> None:
         dto = OrderPaymentSuccessEventDto.from_payload(
                            event=event,
                        )
         
         await self.order_success_handler.execute(dto)
    async def handle_payment_failed(self,  event: dict) -> None:
         dto = OrderPaymentFailureEventDto.from_payload(
         
                             event=event,
                         )
         await self.order_failed_handler.execute(dto)
         
         
         
    async def handle_payment_timeout(self,  event: dict) -> None:
         dto = OrderPaymentTimeoutEventDto.from_payload(
                             event=event,
                         )
         await self.order_timeout_handler.execute(dto)
        