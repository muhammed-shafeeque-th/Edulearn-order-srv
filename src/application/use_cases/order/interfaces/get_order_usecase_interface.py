
  
from abc import ABC, abstractmethod

from src.application.dtos.get_order_dto import GetOrderDto
from src.domain.entities.order import Order


class IGetOrderUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: GetOrderDto) -> Order:
        pass
    
