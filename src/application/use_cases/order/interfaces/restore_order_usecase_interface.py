
  
from abc import ABC, abstractmethod

from src.application.dtos.restore_order_dto import RestoreOrderDto
from src.domain.entities.order import Order


class IRestoreOrderUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: RestoreOrderDto) -> Order:
        pass
    
