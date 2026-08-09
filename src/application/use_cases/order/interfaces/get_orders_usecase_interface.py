
  
from abc import ABC, abstractmethod
from typing import TypedDict

from src.application.dtos.get_orders_by_user_dto import GetOrdersByUserDto
from src.domain.entities.order import Order

class OrdersUseCaseResponse(TypedDict):
    orders: list[Order]
    total: int


class IGetOrdersUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: GetOrdersByUserDto) -> OrdersUseCaseResponse:
        pass
    
