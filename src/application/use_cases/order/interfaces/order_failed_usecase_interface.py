
  
from abc import ABC, abstractmethod

from src.domain.events.order_payment_failure_event import OrderPaymentFailureEventDto


class IOrderFailedUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: OrderPaymentFailureEventDto):
        pass
    
