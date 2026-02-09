import grpc
from grpc import aio
from typing import Any, cast

from typing import TypedDict, List
from src.infrastructure.grpc.generated.course.types.enrollment_pb2 import CheckCourseEnrollmentRequest
from src.infrastructure.grpc.generated.course.types.course_pb2 import GetCourseRequest, GetCoursesByIdsRequest
from src.infrastructure.config.settings import settings
from src.application.interfaces.logging_interface import ILoggingService
from src.infrastructure.grpc.interceptors.client_inerceptors import ClientAuthInterceptor, ClientTracingInterceptor
from src.infrastructure.grpc.generated.course_service_pb2_grpc import CourseServiceStub, EnrollmentServiceStub
from src.application.interfaces.grpc_client_interface import CourseEnrollmentResult, CourseInfo, ICourseServiceClient
from src.infrastructure.grpc.clients.channel_pool import ChannelPool
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from circuitbreaker import circuit


class CourseServiceClient(ICourseServiceClient):
    def __init__(self, logging_service: ILoggingService, token: str | None = None):
        self.pool = ChannelPool(
            settings.COURSE_SERVICE_NAME, settings.COURSE_SERVICE_GRPC, logging_service=logging_service, max_size=10)
        self.logger = logging_service.get_logger("CourseServiceClient")
        self.interceptors = [
            ClientTracingInterceptor(),
            # ClientAuthInterceptor(token) if token else None,
        ]
        self.interceptors = [i for i in self.interceptors if i is not None]

    @circuit(failure_threshold=5, recovery_timeout=30)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get_course(self, course_id: str) -> CourseInfo:
        channel = await self.pool.acquire()
        try:
            from typing import Any, cast
            intercept_fn = getattr(aio, "intercept_channel", None)
            if callable(intercept_fn):
                intercepted = cast(Any, intercept_fn)(
                    channel, *self.interceptors)
            else:
                intercepted = channel
            stub = CourseServiceStub(intercepted)
            request = GetCourseRequest(course_id=course_id)
            response = await stub.GetCourse(request)
            has_error = False
            err = getattr(response, "error", None)
            err_code = getattr(err, "code", "") if err is not None else ""
            err_msg = getattr(
                err, "message", "") if err is not None else ""
            has_error = bool(err_code or err_msg)

            if has_error:
                err = getattr(response, "error", None)
                self.logger.error(
                    f"Failed to get course {course_id}: {getattr(err, 'message', '')}")
                raise ValueError(getattr(err, "message", "Unknown error"))
            
            return {"course_id": response.course.id, "price": response.course.price, "discount_price": getattr(response.course, "discount_price"), "status": getattr(response.course, "status") }
        except Exception as e:
            self.logger.error(f"Failed to get course {course_id}: {str(e)}")
            raise
        finally:
            await self.pool.release(channel)
            
            
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def is_user_enrolled_in_course(self, user_id: str, course_id: str) -> CourseEnrollmentResult:
        """
        Checks if a user is enrolled in a specific course using gRPC.
        Handles channel interception, logging, and error propagation.
        Returns: dict with 'is_enrolled': bool.
        """
        channel = await self.pool.acquire()
        try:
            

            # Proper channel interception for aio/normal compatibility
            intercept_fn = getattr(aio, "intercept_channel", None)
            intercepted_channel = cast(Any, intercept_fn)(
                channel, *self.interceptors) if callable(intercept_fn) else channel

            stub = EnrollmentServiceStub(intercepted_channel)
            request = CheckCourseEnrollmentRequest(course_id=course_id, user_id=user_id)
            response = await stub.CheckCourseEnrollment(request)

            # Unified error detection
            has_error = False
            err = None
            if not has_error:
                err = getattr(response, "error", None)
                err_code = getattr(err, "code", "") if err is not None else ""
                err_msg = getattr(err, "message", "") if err is not None else ""
                has_error = bool(err_code or err_msg)

            if has_error:
                desc = getattr(err, "message", "Unknown error") if err is not None else "Unknown error"
                self.logger.error(f"Failed to check enrollment for user {user_id} in course {course_id}: {desc}")
                raise ValueError(desc)

            # Guard against response structure
            is_enrolled = getattr(response, "enrolled", False)
            return {"is_enrolled": is_enrolled}

        except Exception as e:
            self.logger.error(
                f"Error checking enrollment for user {user_id} in course {course_id}: {str(e)}"
            )
            raise
        finally:
            await self.pool.release(channel)

    @circuit(failure_threshold=5, recovery_timeout=30)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get_courses_by_ids(self, course_ids: list[str]) -> List[CourseInfo]:
        channel = await self.pool.acquire()
        try:
            intercept_fn = getattr(aio, "intercept_channel", None)
            intercepted_channel = cast(Any, intercept_fn)(
                channel, *self.interceptors) if callable(intercept_fn) else channel

            stub = CourseServiceStub(intercepted_channel)
            request = GetCoursesByIdsRequest(course_ids=course_ids)
            response = await stub.GetCourse(request)
            has_error = False
            err = None
            err_msg = ''
            if not has_error:
                err = getattr(response, "error", None)
                err_code = getattr(err, "code", "") if err is not None else ""
                err_msg = getattr(err, "message", "") if err is not None else ""
                has_error = bool(err_code or err_msg)

            if has_error:
                self.logger.error(
                    f"Failed to get courses for {len(course_ids)} courses : {err_msg}")
                raise ValueError(err_msg)
            # self.logger.info("courses ids response " + str(response))
            return [
                {
                    "course_id": course.course_id,
                    "price": course.price,
                    "discount_price": getattr(course, "discount_price", course.price),
                    "status": getattr(response.course, "status")
                }
                for course in getattr(response, "courses", [])
            ]
        except Exception as e:
            self.logger.error(
                f"Failed to get {len(course_ids)} courses with: {str(e)}")
            raise
        finally:
            await self.pool.release(channel)

    async def close(self):
        await self.pool.close()
