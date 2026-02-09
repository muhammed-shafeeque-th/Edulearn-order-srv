import asyncio
import json
from typing import Any
from src.domain.events.order_created_event import OrderCreatedEvent, OrderCreatedEventType
from src.shared.events.topics import EVENT_TOPICS
from src.infrastructure.database.database import get_db
from src.domain.entities.order_items import OrderItem
from src.domain.exceptions.exceptions import CourseAlreadyEnrolledException, UserNotFoundException
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.domain.repositories.order_repository import IOrderRepository
from src.application.dtos.order_create_dto import OrderCreateDto
from src.application.dtos.order_dto import OrderDto
from src.application.interfaces.grpc_client_interface import (
    CourseInfo,
    ICourseServiceClient,
    IUserServiceClient,
)
from src.application.dtos.order_create_dto import OrderCreateDto
from src.application.dtos.order_dto import OrderDto
from src.application.interfaces.kafka_producer_interface import IKafkaProducer
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.metrics_interface import IMetricsService
from src.application.interfaces.redis_interface import IRedisService
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.entities.order import Order, OrderStatus
from src.domain.entities.order_items import OrderItem
from src.domain.exceptions.exceptions import UserNotFoundException
from src.domain.repositories.order_repository import IOrderRepository
from src.domain.value_objects.money import Money
from src.application.dtos.order_create_dto import OrderCreateDto
from src.application.dtos.order_dto import OrderDto
from src.shared.events.topics import EVENT_TOPICS
from src.infrastructure.database.database import get_db
from src.domain.exceptions.exceptions import UserNotFoundException
from uuid import uuid4


class PlaceOrderUseCase:
    CACHE_EXPIRATION_SEC = 3600 # 1hr
    SALES_TAX_RATE = 0.0  # TODO: Set to actual rate, e.g. 0.07 for 7% sales tax

    def __init__(
        self,
        order_repository: IOrderRepository,
        kafka_producer: IKafkaProducer[OrderCreatedEventType],
        course_service_client: ICourseServiceClient,
        user_service_client: IUserServiceClient,
        redis: IRedisService,
        logging_service: ILoggingService,
        metrics_service: IMetricsService,
    ):
        self.order_repository = order_repository
        self.kafka_producer = kafka_producer
        self.course_service_client = course_service_client
        self.user_service_client = user_service_client
        self.redis = redis
        self.logger = logging_service.get_logger("PlaceOrderUseCase")
        self.metrics = metrics_service

    # @retry( stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def execute(self, order_dto: OrderCreateDto, idempotency_key: str | None) -> OrderDto:
        self.logger.info(
            f"Executing PlaceOrderUseCase for user {order_dto.user_id}")

        if idempotency_key:
            async with get_db() as session:
                order = await self.order_repository.find_by_idempotency_key(
                    idempotency_key=idempotency_key, session=session
                )
                if order:
                    self.logger.info(
                        f"Order exists with idempotency_key {idempotency_key}, skipping creation"
                    )
                    return OrderDto.from_domain(order)

        user = await self.user_service_client.get_user(order_dto.user_id)
        if not user:
            raise UserNotFoundException(
                f"User not found with Id {order_dto.user_id}")

        course_ids = order_dto.course_ids

        # await self.ensure_user_not_already_enrolled(order_dto.user_id, course_ids)

        # prices = await self.validate_and_fetch_course_prices(course_ids)

        ensure_task = self.ensure_user_not_already_enrolled(
            order_dto.user_id, course_ids)
        fetch_prices_task = self.validate_and_fetch_course_prices(course_ids)
        _, prices = await asyncio.gather(ensure_task, fetch_prices_task)

        self.logger.info(f"Fetched Prices: {prices}")

        def _to_scu(value: float) -> int:
            """Convert to smallest currency unit (e.g. cents) safely."""
            return int(round(value * 100))

        subtotal = sum(
            _to_scu(prices.get(cid, {}).get("price", 0)) for cid in course_ids
        )

        total_discount = sum(
            max(0, _to_scu(prices.get(cid, {}).get("price", 0)) -
                _to_scu(prices.get(cid, {}).get("discounted_price", prices.get(cid, {}).get("price", 0))))
            for cid in course_ids
        )

        coupon_discount = 0
        coupon_code = getattr(order_dto, "coupon_code", None)

        if coupon_code:
            try:
                self.logger.info(f"Checking coupon code: {coupon_code}")
                # coupon_response = await self.coupon_service_client.validate_and_get_coupon(
                #     coupon_code=coupon_code,
                #     user_id=order_dto.user_id,
                #     course_ids=course_ids,
                #     order_amount=subtotal,
                # )
                coupon_response = {
                    "amount_off": 0.00,
                }
                coupon_discount = int(coupon_response.get(
                    "amount_off", 0))  # in cents

                self.logger.info(
                    f"Coupon {coupon_code} applied. Discount: {coupon_discount}")
            except Exception as e:
                self.logger.error(
                    f"Coupon validation failed or error occurred: {str(e)}")
                coupon_discount = 0

        discounted_subtotal = subtotal - total_discount

        coupon_discount = min(coupon_discount, max(0, discounted_subtotal))
        discounted_total_after_coupon = discounted_subtotal - coupon_discount

        sales_tax = int(
            round(discounted_total_after_coupon * self.SALES_TAX_RATE))

        total = discounted_total_after_coupon + sales_tax

        order_items = [
            OrderItem(
                id=str(uuid4()),
                course_id=cid,
                price=_to_scu(prices.get(cid, {}).get(
                    "discounted_price", prices.get(cid, {}).get("price", 0))),
            )
            for cid in course_ids
        ]

        # log_info = {
        #     "orderItems": [item.__dict__ for item in order_items],
        #     "subtotal": subtotal,
        #     "item_discount": total_discount,
        #     "coupon_discount": coupon_discount,
        #     "discounted_subtotal": discounted_subtotal,
        #     "subtotal_after_coupon": discounted_total_after_coupon,
        #     "tax": sales_tax,
        #     "total": total,
        # }
        # self.logger.info(json.dumps(log_info, indent=2))

        order = Order.create(
            user_id=order_dto.user_id,
            idempotency_key=idempotency_key,
            items=order_items,
            sub_total=subtotal,
            sales_tax=sales_tax,
            amount=Money(amount=total),
            status=OrderStatus.CREATED,
            # total discount includes item + coupon
            discount=total_discount + coupon_discount,
            payment_details=None,
        )

        order.mark_pending_payment()

        async with get_db() as session:
            await self.order_repository.save(order, session)

        self.logger.debug("Order creation request has been successful")

        await self.kafka_producer.publish_event(
            EVENT_TOPICS.ORDER_COURSE_CREATED.value,
            event=OrderCreatedEvent(
                orderId = order.id,
                userId = order.user_id,
                items = [{"courseId": item.course_id, "price": item.price} for item in order.items],
                subtotal=subtotal,
                discount=total_discount,
                coupon_discount=coupon_discount,
                tax=sales_tax,
                total=total,
                currency=order.amount.currency,
            ).to_dict(),
            schema=None,
        )

        return OrderDto.from_domain(order)

    async def validate_and_fetch_course_prices(self, course_ids: list[str]) -> dict[str, dict[str, float]]:
        """
        Retrieve and validate course price info using cache (Redis) as primary source,
        falling back to gRPC calls for uncached courses, and keeping the cache updated.
        Returns: { course_id: {"price": float, "discounted_price": float} }
        Ensures all courses are published, raising a descriptive error if any are not.
        """
        if not course_ids:
            return {}

        cache_keys = [f"course_price:{course_id}" for course_id in course_ids]
        prices: dict[str, dict[str, float]] = {}
        uncached_course_ids: list[str] = []

        async with self.redis.client.pipeline() as pipe:
            for key in cache_keys:
                pipe.get(key)
            cached_prices = await pipe.execute()

        for course_id, cached_value in zip(course_ids, cached_prices):
            if cached_value is not None:
                try:
                    if isinstance(cached_value, bytes):
                        cached_value = cached_value.decode('utf-8')
                    price_obj = json.loads(cached_value)
                    prices[course_id] = {
                        "discounted_price": float(price_obj.get("discounted_price", price_obj.get("price", 0))),
                        "price": float(price_obj.get("price", 0)),
                    }
                    self.metrics.cache_hits(type="course_price")
                except (ValueError, TypeError, KeyError) as e:
                    self.logger.warning(
                        f"Cache parse error for course_id {course_id}: {e}; Value was: {cached_value}"
                    )
                    uncached_course_ids.append(course_id)
            else:
                uncached_course_ids.append(course_id)
                self.metrics.cache_misses(type="course_price")

        if uncached_course_ids:
            batch_supported = hasattr(self.course_service_client, "get_courses_by_ids")
            fetched_dict = {}
            not_published_courses = {}

            if batch_supported:
                try:
                    grpc_results = await self.course_service_client.get_courses_by_ids(uncached_course_ids)
                    for c in grpc_results:
                        status = c.get("status", "unknown")
                        course_id = c["course_id"]
                        if status != "published":
                            not_published_courses[course_id] = status
                            self.logger.warning(
                                f"Course {course_id} is not published (status: {status})"
                            )
                            continue
                        fetched_dict[course_id] = {
                            "discounted_price": float(
                                c.get("discount_price", c.get("price", 0))
                            ),
                            "price": float(c.get("price", 0)),
                        }
                except Exception as e:
                    self.logger.error(
                        f"Batch fetch failed for courses {uncached_course_ids}, falling back to per-course requests: {e}"
                    )
                    fetched_dict = {}
            else:
                fetched_dict = {}
                not_published_courses = {}

            missing_courses = set(uncached_course_ids) - set(fetched_dict.keys()) - set(not_published_courses.keys())
            if missing_courses:
                tasks = [
                    self.course_service_client.get_course(cid) for cid in missing_courses
                ]
                task_results = await asyncio.gather(*tasks, return_exceptions=True)
                for course_id, result in zip(missing_courses, task_results):
                    if isinstance(result, (Exception, BaseException)):
                        self.logger.error(
                            f"Failed to fetch course {course_id}: {str(result)}"
                        )
                        raise result
                    status = result.get("status", "unknown") if hasattr(result, "get") else getattr(result, "status", "unknown")
                    if status != "published":
                        not_published_courses[course_id] = status
                        self.logger.warning(
                            f"Course {course_id} is not published (status: {status})"
                        )
                        continue
                    fetched_dict[course_id] = {
                        "discounted_price": float(getattr(result, "discount_price", 0) if hasattr(result, "discount_price") else result.get("discount_price", 0)),
                        "price": float(getattr(result, "price", 0) if hasattr(result, "price") else result.get("price", 0)),
                    }

            if not_published_courses:
                courses_list = ', '.join(
                    f"{cid} (status: {status})" for cid, status in not_published_courses.items()
                )
                error_message = (
                    f"The following courses are not available for ordering because they are not published: {courses_list}."
                )
                self.logger.error(error_message)
                raise ValueError({
                    "ui_message": "Some selected courses are not available for ordering because they are not published.",
                    "details": error_message
                })

            async with self.redis.client.pipeline() as pipe:
                for course_id, val in fetched_dict.items():
                    prices[course_id] = val
                    pipe.set(
                        f"course_price:{course_id}",
                        json.dumps(val),
                        ex=self.CACHE_EXPIRATION_SEC
                    )
                await pipe.execute()

        return prices

    async def ensure_user_not_already_enrolled(self, user_id: str, course_ids: list[str]) -> None:
        """
        Checks if a user is already enrolled in any of the given courses.
        Raises CourseAlreadyEnrolledException with a user-friendly message if any enrolled.
        """
        if not course_ids:
            return

        tasks = [
            self.course_service_client.is_user_enrolled_in_course(user_id, cid) for cid in course_ids
        ]
        task_results = await asyncio.gather(*tasks, return_exceptions=True)
        enrolled_courses = []
        for course_id, result in zip(course_ids, task_results):
            if isinstance(result, (Exception, BaseException)):
                self.logger.error(
                    f"Failed to fetch course enrollment {course_id}: {str(result)}"
                )
                raise result
            if result.get("is_enrolled", True):
                enrolled_courses.append(course_id)

        if enrolled_courses:
            self.logger.error(
                f"user {user_id} already enrolled into course(s) {', '.join(enrolled_courses)}, aborting"
            )
            raise CourseAlreadyEnrolledException(
                "You are already enrolled in one or more of the selected courses. Please remove the enrolled courses from your order before proceeding."
            )
