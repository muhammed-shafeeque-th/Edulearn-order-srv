
  
from abc import ABC, abstractmethod

from src.application.dtos.order_create_dto import OrderCreateDto
from src.domain.entities.order import Order


class IPlaceOrderUseCase(ABC):
    @abstractmethod
    async def execute(self, order_dto: OrderCreateDto, idempotency_key: str | None) -> Order:
        pass
    
