import json
from datetime import datetime
from typing import Any, Optional, List

from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, func
from sqlalchemy.orm import InstrumentedAttribute, selectinload

from src.domain.entities.order_items import OrderItem
from src.domain.entities.payment_details import PaymentDetails
from src.domain.entities.order import Order, OrderStatus
from src.domain.value_objects.money import Money
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.redis_interface import IRedisService
from src.domain.repositories.order_repository import IOrderRepository, RevenueRange, RevenueStats
from src.infrastructure.database.models.order_model import (
    OrderModel,
    OrderItemModel,
    PaymentDetailsModel,
)
from src.infrastructure.database.database import AsyncSession
from src.infrastructure.database.mappers.entity_mapper import EntityMapper


class SqlOrderRepository(IOrderRepository):
    def __init__(self, redis: IRedisService, logging_service: ILoggingService):
        self.redis = redis
        self.logger = logging_service.get_logger("SqlOrderRepository")

    async def save(self, order: Order, session: AsyncSession) -> Order:
        """
        Upserts OrderModel and relationships, properly managing cache invalidation and persistence.
        """
        try:
            existing = await session.get(
                OrderModel, order.id,
                options=[
                    selectinload(OrderModel.items),
                    selectinload(OrderModel.payment_details)
                ]
            )
            if not existing:
                # Create new model
                order_model = OrderModel(
                    id=order.id,
                    user_id=order.user_id,
                    idempotency_key=order.idempotency_key,
                    amount=order.amount.amount,
                    currency=order.amount.currency,
                    discount=order.discount,
                    sub_total=order.sub_total,
                    sales_tax=order.sales_tax,
                    status=order.status.value if hasattr(
                        order.status, "value") else order.status,
                    created_at=order.created_at,
                    updated_at=order.updated_at,
                )
                order_model.items = [
                    OrderItemModel(
                        id=item.id, course_id=item.course_id, price=item.price)
                    for item in order.items
                ]
                if order.payment_details:
                    order_model.payment_details = EntityMapper.to_orm_payment_details(
                        order.payment_details, order.id)
                session.add(order_model)
                await session.flush()
                await session.refresh(order_model)
                persisted = order_model
            else:
                # Update fields
                for field in ["user_id", "idempotency_key", "amount", "currency","discount", "sub_total", "sales_tax"]:
                    if field == "amount":
                        # This is the float value of order.amount.amount
                        value = getattr(order.amount, "amount", None)
                    elif field == "currency":
                        value = getattr(order.amount, "currency", None)
                    else:
                        value = getattr(order, field, None)
                    setattr(existing, field, value)

                setattr(existing, "status", order.status.value if hasattr(
                    order.status, "value") else order.status)
                setattr(existing, "updated_at",
                        order.updated_at or datetime.utcnow())

                # Replace items
                existing.items[:] = [
                    OrderItemModel(
                        id=item.id, course_id=item.course_id, price=item.price)
                    for item in order.items
                ]

                # Upsert payment details
                if order.payment_details:
                    if existing.payment_details:
                        pd = existing.payment_details
                        pd.payment_id = order.payment_details.payment_id
                        pd.provider = order.payment_details.provider
                        pd.provider_order_id = order.payment_details.provider_order_id
                        pd.payment_status = order.payment_details.payment_status
                        pd.updated_at = order.payment_details.updated_at or datetime.utcnow()
                    else:
                        existing.payment_details = EntityMapper.to_orm_payment_details(
                            order.payment_details, order.id)

                await session.flush()
                await session.refresh(existing)
                persisted = existing

            # Cache housekeeping
            domain_order = EntityMapper.to_domain_order(persisted)
            await self._invalidate_order_caches(domain_order)
            cache_json = EntityMapper.serialize_order_to_json(domain_order)
            cache_key = f"orders:{domain_order.id}"
            await self.redis.set(cache_key, cache_json, expire=3600)
            if domain_order.idempotency_key:
                idem_cache_key = f"orders:idempotency_key:{domain_order.idempotency_key}"
                await self.redis.set(idem_cache_key, cache_json, expire=3600)

            return domain_order
        except IntegrityError as ie:
            self.logger.error(
                "IntegrityError while saving order: %s", getattr(ie, "orig", ie))
            await session.rollback()
            raise
        except Exception as e:
            self.logger.exception(
                f"Failed to save/update order and keep cache in sync: {str(e)}")
            try:
                await session.rollback()
            except Exception:
                pass
            raise

    async def _invalidate_order_caches(self, order: Order):
        """
        Invalidate all cache entries related to an order and the user's paged list caches.
        """
        await self.redis.delete(f"orders:{order.id}")
        if order.idempotency_key:
            await self.redis.delete(f"orders:idempotency_key:{order.idempotency_key}")
        # Invalidate paged user order caches (pattern-based if supported)
        user_cache_pattern = f"user_orders:{order.user_id}:p*:s*:o*"
        try:
            await self.redis.delete_pattern(user_cache_pattern)
        except AttributeError:
            self.logger.warning(
                "RedisService does not implement delete_pattern; paged user orders cache may be stale.")

    async def find_by_id(self, order_id: str, session: AsyncSession) -> Optional[Order]:
        cache_key = f"orders:{order_id}"
        try:
            cached = await self.redis.get(cache_key)
            if cached is not None:
                try:
                    return EntityMapper.deserialize_json_to_order(json.loads(cached))
                except Exception as e:
                    self.logger.warning(
                        f"Invalid/corrupt cache for {cache_key}: {e}")
                    await self.redis.delete(cache_key)
            result = await session.execute(
                select(OrderModel)
                .options(selectinload(OrderModel.items), selectinload(OrderModel.payment_details))
                .where(OrderModel.id == order_id)
            )
            order_model = result.scalars().first()
            if not order_model:
                return None
            order = EntityMapper.to_domain_order(order_model)
            await self.redis.set(cache_key, EntityMapper.serialize_order_to_json(order), expire=3600)
            return order
        except Exception as e:
            self.logger.error(f"Failed to find order {order_id}: {str(e)}")
            raise

    async def find_by_idempotency_key(self, idempotency_key: str, session: AsyncSession) -> Optional[Order]:
        cache_key = f"orders:idempotency_key:{idempotency_key}"
        try:
            cached = await self.redis.get(cache_key)
            if cached:
                try:
                    return EntityMapper.deserialize_json_to_order(json.loads(cached))
                except Exception as e:
                    self.logger.warning(
                        f"Invalid/corrupt idempotency order cache for {cache_key}: {e}")
                    await self.redis.delete(cache_key)

            # DB fallback
            result = await session.execute(
                select(OrderModel)
                .options(selectinload(OrderModel.items), selectinload(OrderModel.payment_details))
                .where(OrderModel.idempotency_key == idempotency_key)
            )
            order_model = result.scalars().first()
            if not order_model:
                return None
            order = EntityMapper.to_domain_order(order_model)
            # Cache for both idempotency key and order id
            order_json = EntityMapper.serialize_order_to_json(order)
            await self.redis.set(cache_key, order_json, expire=3600)
            await self.redis.set(f"orders:{order.id}", order_json, expire=3600)
            return order
        except Exception as e:
            self.logger.error(
                f"Failed to find order with idempotency_key {idempotency_key}: {str(e)}")
            raise

    async def find_by_user_id(
        self,
        user_id: str,
        session: AsyncSession,
        status: Optional[str] = None,
        page: Optional[int] = 1,
        page_size: Optional[int] = 20,
        sort_order: Optional[str] = "desc",
    ) -> tuple[List[Order], int]:

        def map_status_to_db(status: Optional[str]) -> Optional[List[str]]:
            status_map = {
                "pending": ["created", "pending_payment", "processing"],
                "failed": ["failed"],
                "succeeded": ["succeeded"],
                "completed": ["succeeded"],
                "cancelled": ["cancelled", "expired"],
                "refunded": ["refunded"],
                "expired": ["expired", "expired"],
            }
            if status is None:
                return None
            return status_map.get(status.strip().lower())

        # Validate pagination params
        page = page if isinstance(page, int) and page > 0 else 1
        page_size = page_size if isinstance(
            page_size, int) and page_size > 0 else 20
        sort_order = (sort_order or "desc").lower()
        if sort_order not in ("asc", "desc"):
            sort_order = "desc"

        offset = (page - 1) * page_size
        status_segment = status.strip().lower() if status is not None else "all"
        cache_key = f"user_orders:{user_id}:p{page}:s{page_size}:o{sort_order}:status:{status_segment}"

        try:
            # Try cache first
            cached = await self.redis.get(cache_key)
            if cached:
                try:
                    cache_data = json.loads(cached)
                    if not isinstance(cache_data, dict):
                        raise ValueError(f"Cache not dict: {cache_data}")
                    orders_data = cache_data.get("orders", [])
                    if not isinstance(orders_data, list):
                        raise ValueError(
                            f"'orders' not a list: {orders_data!r}")
                    orders = [EntityMapper.deserialize_json_to_order(json.loads(
                        o) if isinstance(o, str) else o) for o in orders_data]
                    total = cache_data.get("total", 0)
                    try:
                        total = int(total)
                    except Exception:
                        total = 0
                    return orders, total
                except Exception as e:
                    self.logger.warning(
                        f"Invalid/corrupt paged user orders cache for {cache_key}: {e}")
                    try:
                        await self.redis.delete(cache_key)
                    except Exception as del_e:
                        self.logger.warning(
                            f"Failed to delete corrupt cache key {cache_key}: {del_e}")

            ordering_col = OrderModel.created_at.asc(
            ) if sort_order == "asc" else OrderModel.created_at.desc()
            mapped_statuses = map_status_to_db(status)
            where_clauses = [OrderModel.user_id == user_id]
            if mapped_statuses:
                where_clauses.append(OrderModel.status.in_(mapped_statuses))

            stmt = (
                select(OrderModel)
                .options(selectinload(OrderModel.items), selectinload(OrderModel.payment_details))
                .where(*where_clauses)
                .order_by(ordering_col)
                .offset(offset)
                .limit(page_size)
            )
            result = await session.execute(stmt)
            order_models = result.scalars().all()
            domain_results = [EntityMapper.to_domain_order(order_model)
                              for order_model in order_models]

            # Total count (respecting status filter)
            count_stmt = select(func.count()).select_from(
                OrderModel).where(*where_clauses)
            total_result = await session.execute(count_stmt)
            total_count = total_result.scalar_one() or 0

            # Cache the results
            to_cache = {
                "orders": [EntityMapper.serialize_order_to_json(order) for order in domain_results],
                "total": total_count
            }
            try:
                await self.redis.set(cache_key, json.dumps(to_cache), expire=1200)
            except Exception as e:
                self.logger.warning(
                    f"Failed to cache user orders for {user_id}: {e}")

            return domain_results, total_count
        except Exception as e:
            self.logger.error(
                f"Failed to find orders for user {user_id} [page={page}, size={page_size}, order={sort_order}, status={status}]: {str(e)}"
            )
            raise

    async def update_status(self, order_id: str, status: str, session: AsyncSession) -> None:
        try:
            await session.execute(
                update(OrderModel)
                .where(OrderModel.id == order_id)
                .values(status=status)
            )
            await session.commit()
            order_model = await session.get(OrderModel, order_id)
            user_id = getattr(order_model, "user_id", None)
            idempotency_key = getattr(order_model, "idempotency_key", None)
            await self.redis.delete(f"orders:{order_id}")
            if idempotency_key and not isinstance(idempotency_key, InstrumentedAttribute):
                await self.redis.delete(f"orders:idempotency_key:{idempotency_key}")
            if user_id and not isinstance(user_id, InstrumentedAttribute):
                try:
                    await self.redis.delete_pattern(f"user_orders:{user_id}:p*:s*:o*")
                except AttributeError:
                    self.logger.warning(
                        "RedisService does not implement delete_pattern; paged user orders cache may be stale.")
        except Exception as e:
            await session.rollback()
            self.logger.error(
                f"Failed to update status for order {order_id}: {str(e)}")
            raise
    
    async def get_revenue_stats(self, range: RevenueRange, session: AsyncSession) -> RevenueStats:
        """
        Calculate revenue statistics based on the specified range.

        Args:
            range (RevenueRange): "thisMonth" or "lastMonth"
            session (AsyncSession): SQLAlchemy async session

        Returns:
            RevenueStats: Dict containing revenue_this_month and revenue_last_month
        """
        try:
            now = datetime.utcnow()
            # Calculate 'this month' start/end
            this_month_start = datetime(now.year, now.month, 1)
            if now.month == 12:
                this_month_end = datetime(now.year + 1, 1, 1)
            else:
                this_month_end = datetime(now.year, now.month + 1, 1)

            # Calculate 'last month' start/end
            if now.month == 1:
                last_month_start = datetime(now.year - 1, 12, 1)
                last_month_end = datetime(now.year, 1, 1)
            else:
                last_month_start = datetime(now.year, now.month - 1, 1)
                last_month_end = this_month_start

            # Use .value to send the raw string to DB, not the Enum itself!
            succeeded_status = OrderStatus.SUCCEEDED.value if hasattr(OrderStatus.SUCCEEDED, "value") else str(OrderStatus.SUCCEEDED)

            stmt_this_month = (
                select(func.coalesce(func.sum(OrderModel.amount), 0.0))
                .where(
                    OrderModel.created_at >= this_month_start,
                    OrderModel.created_at < this_month_end,
                    OrderModel.status == succeeded_status
                )
            )
            stmt_last_month = (
                select(func.coalesce(func.sum(OrderModel.amount), 0.0))
                .where(
                    OrderModel.created_at >= last_month_start,
                    OrderModel.created_at < last_month_end,
                    OrderModel.status == succeeded_status
                )
            )
            result_this_month = await session.execute(stmt_this_month)
            result_last_month = await session.execute(stmt_last_month)
            revenue_this_month = result_this_month.scalar_one()
            revenue_last_month = result_last_month.scalar_one()
            return RevenueStats(
                revenue_this_month=int(revenue_this_month),
                revenue_last_month=int(revenue_last_month),
            )
        except Exception as e:
            await session.rollback()
            self.logger.error(
                f"Failed to get revenue stats: {str(e)}")
            raise 

    async def add_items(self, order_id: str, items: List[OrderItem], session: AsyncSession) -> None:
        try:
            for item in items:
                session.add(EntityMapper.to_orm_order_item(item, order_id))
            await session.commit()
            order_model = await session.get(OrderModel, order_id)
            user_id = getattr(order_model, "user_id", None)
            idempotency_key = getattr(order_model, "idempotency_key", None)
            await self.redis.delete(f"orders:{order_id}")
            if idempotency_key and not isinstance(idempotency_key, InstrumentedAttribute):
                await self.redis.delete(f"orders:idempotency_key:{idempotency_key}")
            if user_id and not isinstance(user_id, InstrumentedAttribute):
                try:
                    await self.redis.delete_pattern(f"user_orders:{user_id}:p*:s*:o*")
                except AttributeError:
                    self.logger.warning(
                        "RedisService does not implement delete_pattern; paged user orders cache may be stale.")
        except Exception as e:
            await session.rollback()
            self.logger.error(
                f"Failed to add items for order {order_id}: {str(e)}")
            raise

    async def attach_payment_details(
        self,
        order_id: str,
        payment_details: PaymentDetails,
        session: AsyncSession
    ) -> None:
        try:
            order_model = await session.get(OrderModel, order_id, options=[selectinload(OrderModel.payment_details)])
            if not order_model:
                raise ValueError(f"Order {order_id} not found")
            if order_model.payment_details:
                pd = order_model.payment_details
                pd.payment_id = payment_details.payment_id
                pd.provider = payment_details.provider
                pd.provider_order_id = payment_details.provider_order_id
                pd.payment_status = payment_details.payment_status
                pd.updated_at = payment_details.updated_at or datetime.utcnow()
            else:
                model = EntityMapper.to_orm_payment_details(
                    payment_details, order_id)
                order_model.payment_details = model
                session.add(model)
            await session.flush()

            user_id = getattr(order_model, "user_id", None)
            idempotency_key = getattr(order_model, "idempotency_key", None)
            await self.redis.delete(f"orders:{order_id}")
            if idempotency_key and not isinstance(idempotency_key, InstrumentedAttribute):
                await self.redis.delete(f"orders:idempotency_key:{idempotency_key}")
            if user_id and not isinstance(user_id, InstrumentedAttribute):
                try:
                    await self.redis.delete_pattern(f"user_orders:{user_id}:p*:s*:o*")
                except AttributeError:
                    self.logger.warning(
                        "RedisService does not implement delete_pattern; paged user orders cache may be stale.")
        except Exception as e:
            await session.rollback()
            self.logger.error(
                f"Failed to attach payment details for order {order_id}: {str(e)}")
            raise
