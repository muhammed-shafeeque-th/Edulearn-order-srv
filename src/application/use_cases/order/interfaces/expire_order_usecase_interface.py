
  
from abc import ABC, abstractmethod

class IExpireOrderUseCase(ABC):
    @abstractmethod
    async def execute(self, order_id: str):
        pass
    
