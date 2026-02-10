from abc import ABC, abstractmethod
from typing import List, Literal, TypedDict


CourseStatus = Literal["published", "unpublished", "deleted", "draft"]


class CourseInfo(TypedDict):
    course_id: str
    status: CourseStatus
    price: float
    discount_price: float


class CourseEnrollmentResult(TypedDict):
    is_enrolled: bool


class IUserServiceClient(ABC):
    @abstractmethod
    async def get_user(self, user_id: str) -> dict:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class ICourseServiceClient(ABC):
    @abstractmethod
    async def get_course(self, course_id: str) -> CourseInfo:
        pass

    @abstractmethod
    async def is_user_enrolled_in_course(self, user_id: str, course_id: str) -> CourseEnrollmentResult:
        pass

    @abstractmethod
    async def get_courses_by_ids(self, course_ids: list[str]) -> List[CourseInfo]:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class ISessionServiceClient(ABC):
    @abstractmethod
    async def get_session(self, session_id: str) -> dict:
        pass

    @abstractmethod
    async def get_available_slots(self, session_id: str) -> int:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
