
  
from abc import ABC, abstractmethod
from typing import List, TypedDict

from src.domain.repositories.order_repository import RevenueStats
from src.application.dtos.get_orders_by_user_dto import GetOrdersByUserDto


class IGetRevenueStatsUseCase(ABC):
    @abstractmethod
    async def execute(self, year: int) -> List[RevenueStats]:
            """
            Executes the use case to retrieve revenue statistics for a given range.
            
            Args:
                range (RevenueRange): The range for which to get revenue statistics ("thisMonth", "lastMonth").
            
            Returns:
                list: Revenue statistics for the specified period.
            """
            pass
    
