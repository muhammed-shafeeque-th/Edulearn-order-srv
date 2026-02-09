from abc import ABC, abstractmethod
from typing import Literal, Optional, List, TypedDict

from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entities.order import Order
from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails


RevenueRange = Literal["thisMonth", "lastMonth"]


class RevenueStats(TypedDict):
    revenue_this_month: int
    revenue_last_month: int


# This class is an abstract base class for an order repository interface in Python.
class IOrderRepository(ABC):
    @abstractmethod
    async def save(self, order: Order, session: AsyncSession) -> Order:
        """
        The `save` function in Python is an asynchronous method that saves an order object.

        :param order: Order object that contains information about a customer's order, such as items
        purchased, quantity, price, and any other relevant details
        :type order: Order
        """
        pass

    @abstractmethod
    async def find_by_id(self, order_id: str, session: AsyncSession) -> Optional[Order]:
        """
        Asynchronously retrieves an order by its unique identifier.
        Returns the order if found, otherwise returns None.

        Args:
            order_id (str): The unique identifier of the order.

        Returns:
            Optional[Order]: The order object if found, otherwise None.
        """
        pass
    @abstractmethod
    async def find_by_idempotency_key(self, idempotency_key: str, session: AsyncSession) -> Optional[Order]:
        """
        Asynchronously retrieves an order by idempotency key.
        Returns the order if found, otherwise returns None.

        Args:
            idempotency_key (str): A unique identifier.

        Returns:
            Optional[Order]: The order object if found, otherwise None.
        """
        pass


    @abstractmethod
    async def find_by_user_id(
        self,
        user_id: str,
        session: AsyncSession,
        status: str | None = None,
        page: int | None = 1,
        page_size: int | None = 20,
        sort_order: str | None = "desc"
    ) -> tuple[list[Order], int]:
        """
        Fetch orders for a specific user, with pagination and sorting.
        Uses Redis cache for optimization. Falls back to DB if not cached.
        Results are cached per query parameters.
        Args:
            user_id: The user to fetch orders for.
            session: An active SQLAlchemy AsyncSession.
            page: The page number (1-based).
            page_size: The number of items per page.
            sort_order: Either "asc" or "desc" for ordering by creation.
        Returns:
            tuple[list[Order], int]: A tuple of the list of orders matching the query and the total number of orders.
        """
        pass

    @abstractmethod
    async def update_status(self, order_id: str, status: str, session: AsyncSession) -> None:
        """
        Update the status of an order.

        Args:
            order_id (str): The unique identifier of the order.
            status (str): The new status value.
        """
        pass

    @abstractmethod
    async def add_items(self, order_id: str, items: List[OrderItem], session: AsyncSession) -> None:
        """
        Add one or more items to an order.

        Args:
            order_id (str): The unique identifier of the order.
            items (List[OrderItem]): Items to add.
        """
        pass

    @abstractmethod
    async def attach_payment_details(self, order_id: str, payment_details: PaymentDetails, session: AsyncSession) -> None:
        """
        Attach payment details to an order (one-to-one).

        Args:
            order_id (str): The unique identifier of the order.
            payment_details (PaymentDetails): Payment details to attach.
        """
        pass
    @abstractmethod
    async def get_revenue_stats(
        self, 
        range: RevenueRange, 
        session: AsyncSession
    ) -> RevenueStats:
        """
        Calculate revenue statistics for orders within a specified date range.

        Args:
            range (Literal["thisMonth", "lastMonth"]): The range for which to calculate revenue stats.
            session (AsyncSession): An active SQLAlchemy async session.

        Returns:
            RevenueStats: A dictionary containing revenue stats, e.g., 
                  {"revenue_this_month": int, "revenue_last_month": int}
        """
        pass


