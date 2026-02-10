from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from . import course_pb2 as _course_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnrollmentData(_message.Message):
    __slots__ = ("id", "user_id", "course_id", "status", "progress", "enrolled_at", "completed_at", "created_at", "updated_at", "deleted_at", "course")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ENROLLED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    COURSE_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    course_id: str
    status: str
    progress: float
    enrolled_at: str
    completed_at: str
    created_at: str
    updated_at: str
    deleted_at: str
    course: EnrollmentCourseData
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., course_id: _Optional[str] = ..., status: _Optional[str] = ..., progress: _Optional[float] = ..., enrolled_at: _Optional[str] = ..., completed_at: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., course: _Optional[_Union[EnrollmentCourseData, _Mapping]] = ...) -> None: ...

class EnrollmentCourseData(_message.Message):
    __slots__ = ("id", "title", "rating", "thumbnail", "category", "level", "lessonsCount", "instructor")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LESSONSCOUNT_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    rating: int
    thumbnail: str
    category: str
    level: str
    lessonsCount: int
    instructor: _common_pb2.User
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., rating: _Optional[int] = ..., thumbnail: _Optional[str] = ..., category: _Optional[str] = ..., level: _Optional[str] = ..., lessonsCount: _Optional[int] = ..., instructor: _Optional[_Union[_common_pb2.User, _Mapping]] = ...) -> None: ...

class EnrollmentDetail(_message.Message):
    __slots__ = ("enrollment_id", "user_id", "course_id", "progress_percent", "status", "enrolled_at", "sections")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_PERCENT_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ENROLLED_AT_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    course_id: str
    progress_percent: int
    status: str
    enrolled_at: str
    sections: _containers.RepeatedCompositeFieldContainer[EnrollmentSection]
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., course_id: _Optional[str] = ..., progress_percent: _Optional[int] = ..., status: _Optional[str] = ..., enrolled_at: _Optional[str] = ..., sections: _Optional[_Iterable[_Union[EnrollmentSection, _Mapping]]] = ...) -> None: ...

class EnrollmentSection(_message.Message):
    __slots__ = ("id", "title", "description", "order", "is_published", "lessons", "quiz")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    QUIZ_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    order: int
    is_published: bool
    lessons: _containers.RepeatedCompositeFieldContainer[LessonProgress]
    quiz: QuizProgress
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., order: _Optional[int] = ..., is_published: bool = ..., lessons: _Optional[_Iterable[_Union[LessonProgress, _Mapping]]] = ..., quiz: _Optional[_Union[QuizProgress, _Mapping]] = ...) -> None: ...

class LessonProgress(_message.Message):
    __slots__ = ("id", "title", "order", "duration", "completed", "completed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    order: int
    duration: int
    completed: bool
    completed_at: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., order: _Optional[int] = ..., duration: _Optional[int] = ..., completed: bool = ..., completed_at: _Optional[str] = ...) -> None: ...

class QuestionOption(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

class QuizQuestion(_message.Message):
    __slots__ = ("id", "requirePassingScore", "options", "timeLimit", "question", "type", "explanation", "score", "correct_answer")
    ID_FIELD_NUMBER: _ClassVar[int]
    REQUIREPASSINGSCORE_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    TIMELIMIT_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    CORRECT_ANSWER_FIELD_NUMBER: _ClassVar[int]
    id: str
    requirePassingScore: bool
    options: _containers.RepeatedCompositeFieldContainer[QuestionOption]
    timeLimit: int
    question: str
    type: str
    explanation: str
    score: int
    correct_answer: str
    def __init__(self, id: _Optional[str] = ..., requirePassingScore: bool = ..., options: _Optional[_Iterable[_Union[QuestionOption, _Mapping]]] = ..., timeLimit: _Optional[int] = ..., question: _Optional[str] = ..., type: _Optional[str] = ..., explanation: _Optional[str] = ..., score: _Optional[int] = ..., correct_answer: _Optional[str] = ...) -> None: ...

class QuizProgress(_message.Message):
    __slots__ = ("id", "title", "description", "questions", "time_limit", "require_passing_score", "passing_score", "completed", "passed", "score", "completed_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    TIME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    REQUIRE_PASSING_SCORE_FIELD_NUMBER: _ClassVar[int]
    PASSING_SCORE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    description: str
    questions: _containers.RepeatedCompositeFieldContainer[QuizQuestion]
    time_limit: int
    require_passing_score: bool
    passing_score: int
    completed: bool
    passed: bool
    score: int
    completed_at: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., questions: _Optional[_Iterable[_Union[QuizQuestion, _Mapping]]] = ..., time_limit: _Optional[int] = ..., require_passing_score: bool = ..., passing_score: _Optional[int] = ..., completed: bool = ..., passed: bool = ..., score: _Optional[int] = ..., completed_at: _Optional[str] = ...) -> None: ...

class CreateEnrollmentRequest(_message.Message):
    __slots__ = ("user_id", "course_id")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    course_id: str
    def __init__(self, user_id: _Optional[str] = ..., course_id: _Optional[str] = ...) -> None: ...

class GetEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class UpdateEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "status")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    status: str
    def __init__(self, enrollment_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class DeleteEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id",)
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    def __init__(self, enrollment_id: _Optional[str] = ...) -> None: ...

class CheckEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class CheckCourseEnrollmentRequest(_message.Message):
    __slots__ = ("course_id", "user_id")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    user_id: str
    def __init__(self, course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetEnrollmentsByUserRequest(_message.Message):
    __slots__ = ("user_id", "pagination")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    pagination: _common_pb2.Pagination
    def __init__(self, user_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ...) -> None: ...

class GetEnrollmentsByCourseRequest(_message.Message):
    __slots__ = ("course_id", "pagination")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    pagination: _common_pb2.Pagination
    def __init__(self, course_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ...) -> None: ...

class EnrollmentResponse(_message.Message):
    __slots__ = ("enrollment", "error")
    ENROLLMENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    enrollment: EnrollmentData
    error: _common_pb2.Error
    def __init__(self, enrollment: _Optional[_Union[EnrollmentData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class EnrollmentsData(_message.Message):
    __slots__ = ("enrollments", "total")
    ENROLLMENTS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    enrollments: _containers.RepeatedCompositeFieldContainer[EnrollmentData]
    total: int
    def __init__(self, enrollments: _Optional[_Iterable[_Union[EnrollmentData, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class EnrollmentsResponse(_message.Message):
    __slots__ = ("enrollments", "error")
    ENROLLMENTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    enrollments: EnrollmentsData
    error: _common_pb2.Error
    def __init__(self, enrollments: _Optional[_Union[EnrollmentsData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class GetEnrollmentResponse(_message.Message):
    __slots__ = ("enrollment", "error")
    ENROLLMENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    enrollment: EnrollmentData
    error: _common_pb2.Error
    def __init__(self, enrollment: _Optional[_Union[EnrollmentData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class GetEnrollmentDetailsResponse(_message.Message):
    __slots__ = ("enrollment", "error")
    ENROLLMENT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    enrollment: EnrollmentDetail
    error: _common_pb2.Error
    def __init__(self, enrollment: _Optional[_Union[EnrollmentDetail, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteEnrollmentResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class CheckEnrollmentResponse(_message.Message):
    __slots__ = ("enrolled", "error")
    ENROLLED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    enrolled: bool
    error: _common_pb2.Error
    def __init__(self, enrolled: bool = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
