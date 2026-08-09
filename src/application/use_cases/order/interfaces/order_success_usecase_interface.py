
  
from abc import ABC, abstractmethod

from src.domain.events.order_payment_success_event import OrderPaymentSuccessEventDto


class IOrderSuccessUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: OrderPaymentSuccessEventDto):
        pass
    
