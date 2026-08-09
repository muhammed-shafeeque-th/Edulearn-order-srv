
  
from abc import ABC, abstractmethod

from src.domain.events.order_payment_timeout_event import OrderPaymentTimeoutEventDto


class IOrderTimeoutUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: OrderPaymentTimeoutEventDto):
        pass
    
