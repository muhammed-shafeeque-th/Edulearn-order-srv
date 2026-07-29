import json
from src.application.interfaces.logging_interface import ILoggingService
from src.application.interfaces.redis_interface import IRedisService
from src.domain.repositories.session_booking_repository import (
    ISessionBookingRepository,
)
from src.domain.entities.session_booking import SessionBooking
from src.domain.value_objects.money import Money
from src.infrastructure.database.database import AsyncSession
from src.infrastructure.database.models.session_booking_model import SessionBookingModel
from sqlalchemy import select, update, func
from sqlalchemy.exc import IntegrityError
from typing import Optional, List
import logging
from uuid import uuid4
from datetime import datetime


class SqlSessionBookingRepository(ISessionBookingRepository):
    def __init__(self, session: AsyncSession, redis: IRedisService, logging_service: ILoggingService):
        self.session = session
        self.logger = logging_service.get_logger("SqlSessionBookingRepository")
        self.redis = redis

    async def save(self, booking: SessionBooking) -> None:
        try:
            booking_model = SessionBookingModel(
                id=booking.id or str(uuid4()),
                user_id=booking.user_id,
                session_id=booking.session_id,
                amount=booking.amount.amount,
                currency=booking.amount.currency,
                status=booking.status,
                created_at=booking.created_at or datetime.utcnow(),
                updated_at=booking.updated_at or datetime.utcnow(),
                version=booking.version,
            )
            try:
                self.session.add(booking_model)
                await self.session.commit()
            except IntegrityError:
                await self.session.rollback()
                raise ValueError("Optimistic lock failed: booking was modified by another transaction")
            
            session_booking_dto = booking_model.map_to_domain()
            booking.id = session_booking_dto.id
            booking.created_at = session_booking_dto.created_at
            booking.updated_at = session_booking_dto.updated_at
            booking.version = session_booking_dto.version

            # Update cache
            cache_key = f"booking:{booking.id}"
            await self.redis.set(
                cache_key,
                json.dumps(
                    {
                        "id": booking.id,
                        "user_id": booking.user_id,
                        "session_id": booking.session_id,
                        "amount": booking.amount.amount,
                        "currency": booking.amount.currency,
                        "status": booking.status,
                        "version": booking.version,
                        "created_at": booking.created_at.isoformat(),
                        "updated_at": booking.updated_at.isoformat(),
                    }
                ),
                expire=3600,
            )

        except Exception as e:
            self.logger.error(f"Failed to save session booking {booking.id}: {str(e)}")
            await self.session.rollback()
            raise

    async def find_by_id(self, booking_id: str) -> Optional[SessionBooking]:
        try:
            # Check cache first
            cache_key = f"booking:{booking_id}"
            cached_booking = await self.redis.get(cache_key)
            if cached_booking:
                booking_data = json.loads(cached_booking)
                return SessionBooking(
                    id=booking_data["id"],
                    user_id=booking_data["user_id"],
                    session_id=booking_data["session_id"],
                    amount=Money(
                        amount=booking_data["amount"], currency=booking_data["currency"]
                    ),
                    status=booking_data["status"],
                    version=booking_data["version"],
                    created_at=datetime.fromisoformat(booking_data["created_at"]),
                    updated_at=datetime.fromisoformat(booking_data["updated_at"]),
                )

            # Fetch from database
            result = await self.session.execute(
                select(SessionBookingModel).where(SessionBookingModel.id == booking_id)
            )
            booking_model = result.scalars().first()
            if not booking_model:
                return None
            booking_result = booking_model.map_to_domain()
            # Cache the result
            await self.redis.set(
                cache_key,
                json.dumps(
                    {
                        "id": booking_result.id,
                        "user_id": booking_result.user_id,
                        "session_id": booking_result.session_id,
                        "amount": booking_result.amount.amount,
                        "currency": booking_result.amount.currency,
                        "status": booking_result.status,
                        "version": booking_result.version,
                        "created_at": booking_result.created_at.isoformat(),
                        "updated_at": booking_result.updated_at.isoformat(),
                    }
                ),
                expire=3600,
            )

        except Exception as e:
            self.logger.error(f"Failed to find session booking {booking_id}: {str(e)}")
            raise

    async def find_by_session_id(self, session_id: str) -> List[SessionBooking]:
        # Check cache first
        cache_key = f"session_bookings:{session_id}"
        cached_bookings = await self.redis.get(cache_key)
        if cached_bookings:
            bookings_data = json.loads(cached_bookings)
            return [
                SessionBooking(
                    id=booking_data["id"],
                    user_id=booking_data["user_id"],
                    session_id=booking_data["session_id"],
                    amount=Money(
                        amount=booking_data["amount"], currency=booking_data["currency"]
                    ),
                    status=booking_data["status"],
                    version=booking_data["version"],
                    created_at=datetime.fromisoformat(booking_data["created_at"]),
                    updated_at=datetime.fromisoformat(booking_data["updated_at"]),
                )
                for booking_data in bookings_data
            ]

        # Fetch from database
        result = await self.session.execute(
            select(SessionBookingModel).where(
                SessionBookingModel.session_id == session_id
            )
        )
        bookings = result.scalars().all()

        domain_result = [booking.map_to_domain() for booking in bookings]

        # Cache the domain_result
        await self.redis.set(
            cache_key,
            json.dumps(
                [
                    {
                        "id": booking.id,
                        "user_id": booking.user_id,
                        "session_id": booking.session_id,
                        "amount": booking.amount.amount,
                        "currency": booking.amount.currency,
                        "status": booking.status,
                        "version": booking.version,
                        "created_at": booking.created_at.isoformat(),
                        "updated_at": booking.updated_at.isoformat(),
                    }
                    for booking in domain_result
                ]
            ),
            expire=3600,
        )

        return domain_result

    async def find_by_user_id(self, user_id: str) -> List[SessionBooking]:
        try:
            result = await self.session.execute(
                select(SessionBookingModel).where(
                    SessionBookingModel.user_id == user_id
                )
            )
            bookings = result.scalars().all()
            return [booking_model.map_to_domain() for booking_model in bookings]
        except Exception as e:
            self.logger.error(
                f"Failed to find session bookings for user {user_id}: {str(e)}"
            )
            raise

    async def count_bookings_for_session(self, session_id: str) -> int:
        try:
            result = await self.session.execute(
                select(func.count()).where(
                    SessionBookingModel.session_id == session_id,
                    SessionBookingModel.status.in_(["PENDING", "CONFIRMED"]),
                )
            )
            return result.scalar() or 0
        except Exception as e:
            self.logger.error(
                f"Failed to count bookings for session {session_id}: {str(e)}"
            )
            raise
