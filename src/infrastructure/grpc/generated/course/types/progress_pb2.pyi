from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EnrollmentProgressData(_message.Message):
    __slots__ = ("enrollmentId", "courseId", "userId", "overallProgress", "completedUnits", "totalUnits", "lessons", "quizzes")
    ENROLLMENTID_FIELD_NUMBER: _ClassVar[int]
    COURSEID_FIELD_NUMBER: _ClassVar[int]
    USERID_FIELD_NUMBER: _ClassVar[int]
    OVERALLPROGRESS_FIELD_NUMBER: _ClassVar[int]
    COMPLETEDUNITS_FIELD_NUMBER: _ClassVar[int]
    TOTALUNITS_FIELD_NUMBER: _ClassVar[int]
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    QUIZZES_FIELD_NUMBER: _ClassVar[int]
    enrollmentId: str
    courseId: str
    userId: str
    overallProgress: int
    completedUnits: int
    totalUnits: int
    lessons: _containers.RepeatedCompositeFieldContainer[LessonProgress]
    quizzes: _containers.RepeatedCompositeFieldContainer[QuizProgress]
    def __init__(self, enrollmentId: _Optional[str] = ..., courseId: _Optional[str] = ..., userId: _Optional[str] = ..., overallProgress: _Optional[int] = ..., completedUnits: _Optional[int] = ..., totalUnits: _Optional[int] = ..., lessons: _Optional[_Iterable[_Union[LessonProgress, _Mapping]]] = ..., quizzes: _Optional[_Iterable[_Union[QuizProgress, _Mapping]]] = ...) -> None: ...

class LessonProgress(_message.Message):
    __slots__ = ("lessonId", "completed", "completedAt", "watchTime", "duration", "progressPercent")
    LESSONID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    COMPLETEDAT_FIELD_NUMBER: _ClassVar[int]
    WATCHTIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    PROGRESSPERCENT_FIELD_NUMBER: _ClassVar[int]
    lessonId: str
    completed: bool
    completedAt: str
    watchTime: int
    duration: int
    progressPercent: int
    def __init__(self, lessonId: _Optional[str] = ..., completed: bool = ..., completedAt: _Optional[str] = ..., watchTime: _Optional[int] = ..., duration: _Optional[int] = ..., progressPercent: _Optional[int] = ...) -> None: ...

class QuizProgress(_message.Message):
    __slots__ = ("quizId", "completed", "score", "attempts", "passed", "completedAt")
    QUIZID_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    COMPLETEDAT_FIELD_NUMBER: _ClassVar[int]
    quizId: str
    completed: bool
    score: int
    attempts: int
    passed: bool
    completedAt: str
    def __init__(self, quizId: _Optional[str] = ..., completed: bool = ..., score: _Optional[int] = ..., attempts: _Optional[int] = ..., passed: bool = ..., completedAt: _Optional[str] = ...) -> None: ...

class Milestone(_message.Message):
    __slots__ = ("id", "type", "achievedAt")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ACHIEVEDAT_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    achievedAt: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., achievedAt: _Optional[str] = ...) -> None: ...

class UpdateLessonProgressResponseData(_message.Message):
    __slots__ = ("completed", "progressPercent", "milestone")
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    PROGRESSPERCENT_FIELD_NUMBER: _ClassVar[int]
    MILESTONE_FIELD_NUMBER: _ClassVar[int]
    completed: bool
    progressPercent: int
    milestone: Milestone
    def __init__(self, completed: bool = ..., progressPercent: _Optional[int] = ..., milestone: _Optional[_Union[Milestone, _Mapping]] = ...) -> None: ...

class UpdateLessonProgressResponse(_message.Message):
    __slots__ = ("progress", "error")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    progress: UpdateLessonProgressResponseData
    error: _common_pb2.Error
    def __init__(self, progress: _Optional[_Union[UpdateLessonProgressResponseData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class SubmitQuizAttemptResponse(_message.Message):
    __slots__ = ("progress", "error")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    progress: QuizAttemptResponseData
    error: _common_pb2.Error
    def __init__(self, progress: _Optional[_Union[QuizAttemptResponseData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class QuizAttemptResponseData(_message.Message):
    __slots__ = ("score", "passed", "completed", "attempts", "milestone")
    SCORE_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    MILESTONE_FIELD_NUMBER: _ClassVar[int]
    score: int
    passed: bool
    completed: bool
    attempts: int
    milestone: Milestone
    def __init__(self, score: _Optional[int] = ..., passed: bool = ..., completed: bool = ..., attempts: _Optional[int] = ..., milestone: _Optional[_Union[Milestone, _Mapping]] = ...) -> None: ...

class UpdateLessonProgressRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id", "lesson_id", "currentTime", "duration", "event")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENTTIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    lesson_id: str
    currentTime: int
    duration: int
    event: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., lesson_id: _Optional[str] = ..., currentTime: _Optional[int] = ..., duration: _Optional[int] = ..., event: _Optional[str] = ...) -> None: ...

class SubmitQuizAttemptRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id", "quiz_id", "answers", "timeSpent")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    QUIZ_ID_FIELD_NUMBER: _ClassVar[int]
    ANSWERS_FIELD_NUMBER: _ClassVar[int]
    TIMESPENT_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    quiz_id: str
    answers: _containers.RepeatedCompositeFieldContainer[QuizAnswers]
    timeSpent: int
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., quiz_id: _Optional[str] = ..., answers: _Optional[_Iterable[_Union[QuizAnswers, _Mapping]]] = ..., timeSpent: _Optional[int] = ...) -> None: ...

class QuizAnswers(_message.Message):
    __slots__ = ("question_id", "answers")
    QUESTION_ID_FIELD_NUMBER: _ClassVar[int]
    ANSWERS_FIELD_NUMBER: _ClassVar[int]
    question_id: str
    answers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, question_id: _Optional[str] = ..., answers: _Optional[_Iterable[str]] = ...) -> None: ...

class CreateProgressRequest(_message.Message):
    __slots__ = ("enrollment_id", "lesson_id", "progress")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    lesson_id: str
    progress: float
    def __init__(self, enrollment_id: _Optional[str] = ..., lesson_id: _Optional[str] = ..., progress: _Optional[float] = ...) -> None: ...

class GetEnrollmentDetailsRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetProgressRequest(_message.Message):
    __slots__ = ("progress_id",)
    PROGRESS_ID_FIELD_NUMBER: _ClassVar[int]
    progress_id: str
    def __init__(self, progress_id: _Optional[str] = ...) -> None: ...

class UpdateProgressRequest(_message.Message):
    __slots__ = ("progress_id", "progress", "completed")
    PROGRESS_ID_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    progress_id: str
    progress: float
    completed: bool
    def __init__(self, progress_id: _Optional[str] = ..., progress: _Optional[float] = ..., completed: bool = ...) -> None: ...

class DeleteProgressRequest(_message.Message):
    __slots__ = ("progress_id",)
    PROGRESS_ID_FIELD_NUMBER: _ClassVar[int]
    progress_id: str
    def __init__(self, progress_id: _Optional[str] = ...) -> None: ...

class GetProgressByEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class ProgressData(_message.Message):
    __slots__ = ("id", "enrollment_id", "lesson_id", "deleted_at", "completed", "completed_at", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    enrollment_id: str
    lesson_id: str
    deleted_at: str
    completed: bool
    completed_at: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., enrollment_id: _Optional[str] = ..., lesson_id: _Optional[str] = ..., deleted_at: _Optional[str] = ..., completed: bool = ..., completed_at: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ProgressResponse(_message.Message):
    __slots__ = ("progress", "error")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    progress: ProgressData
    error: _common_pb2.Error
    def __init__(self, progress: _Optional[_Union[ProgressData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class EnrollmentProgressResponse(_message.Message):
    __slots__ = ("progress", "error")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    progress: EnrollmentProgressData
    error: _common_pb2.Error
    def __init__(self, progress: _Optional[_Union[EnrollmentProgressData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class ProgressesData(_message.Message):
    __slots__ = ("progresses",)
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    progresses: _containers.RepeatedCompositeFieldContainer[ProgressData]
    def __init__(self, progresses: _Optional[_Iterable[_Union[ProgressData, _Mapping]]] = ...) -> None: ...

class ProgressesResponse(_message.Message):
    __slots__ = ("progresses", "error")
    PROGRESSES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    progresses: ProgressesData
    error: _common_pb2.Error
    def __init__(self, progresses: _Optional[_Union[ProgressesData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteProgressResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
