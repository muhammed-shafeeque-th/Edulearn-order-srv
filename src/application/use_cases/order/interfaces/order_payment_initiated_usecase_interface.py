
  
from abc import ABC, abstractmethod

from src.domain.events.order_payment_initiate_event import OrderPaymentInitiatedEventDto


class IOrderPaymentInitiatedUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: OrderPaymentInitiatedEventDto):
        pass
    
