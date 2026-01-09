from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QuestionOption(_message.Message):
    __slots__ = ("value", "is_correct")
    VALUE_FIELD_NUMBER: _ClassVar[int]
    IS_CORRECT_FIELD_NUMBER: _ClassVar[int]
    value: str
    is_correct: bool
    def __init__(self, value: _Optional[str] = ..., is_correct: bool = ...) -> None: ...

class Question(_message.Message):
    __slots__ = ("id", "type", "points", "time_limit", "question", "required", "options", "correct_answer", "explanation")
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    TIME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    QUESTION_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    CORRECT_ANSWER_FIELD_NUMBER: _ClassVar[int]
    EXPLANATION_FIELD_NUMBER: _ClassVar[int]
    id: str
    type: str
    points: int
    time_limit: int
    question: str
    required: bool
    options: _containers.RepeatedCompositeFieldContainer[QuestionOption]
    correct_answer: str
    explanation: str
    def __init__(self, id: _Optional[str] = ..., type: _Optional[str] = ..., points: _Optional[int] = ..., time_limit: _Optional[int] = ..., question: _Optional[str] = ..., required: bool = ..., options: _Optional[_Iterable[_Union[QuestionOption, _Mapping]]] = ..., correct_answer: _Optional[str] = ..., explanation: _Optional[str] = ...) -> None: ...

class CreateQuizRequest(_message.Message):
    __slots__ = ("course_id", "user_id", "section_id", "description", "title", "isRequired", "time_limit", "passing_score", "max_attempts", "questions")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ISREQUIRED_FIELD_NUMBER: _ClassVar[int]
    TIME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    PASSING_SCORE_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    user_id: str
    section_id: str
    description: str
    title: str
    isRequired: bool
    time_limit: int
    passing_score: int
    max_attempts: int
    questions: _containers.RepeatedCompositeFieldContainer[Question]
    def __init__(self, course_id: _Optional[str] = ..., user_id: _Optional[str] = ..., section_id: _Optional[str] = ..., description: _Optional[str] = ..., title: _Optional[str] = ..., isRequired: bool = ..., time_limit: _Optional[int] = ..., passing_score: _Optional[int] = ..., max_attempts: _Optional[int] = ..., questions: _Optional[_Iterable[_Union[Question, _Mapping]]] = ...) -> None: ...

class GetQuizRequest(_message.Message):
    __slots__ = ("quiz_id",)
    QUIZ_ID_FIELD_NUMBER: _ClassVar[int]
    quiz_id: str
    def __init__(self, quiz_id: _Optional[str] = ...) -> None: ...

class UpdateQuizRequest(_message.Message):
    __slots__ = ("quiz_id", "course_id", "user_id", "description", "title", "isRequired", "time_limit", "passing_score", "max_attempts", "questions")
    QUIZ_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    ISREQUIRED_FIELD_NUMBER: _ClassVar[int]
    TIME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    PASSING_SCORE_FIELD_NUMBER: _ClassVar[int]
    MAX_ATTEMPTS_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    quiz_id: str
    course_id: str
    user_id: str
    description: str
    title: str
    isRequired: bool
    time_limit: int
    passing_score: int
    max_attempts: int
    questions: _containers.RepeatedCompositeFieldContainer[Question]
    def __init__(self, quiz_id: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ..., description: _Optional[str] = ..., title: _Optional[str] = ..., isRequired: bool = ..., time_limit: _Optional[int] = ..., passing_score: _Optional[int] = ..., max_attempts: _Optional[int] = ..., questions: _Optional[_Iterable[_Union[Question, _Mapping]]] = ...) -> None: ...

class DeleteQuizRequest(_message.Message):
    __slots__ = ("quiz_id", "course_id", "user_id")
    QUIZ_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    quiz_id: str
    course_id: str
    user_id: str
    def __init__(self, quiz_id: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetQuizzesByCourseRequest(_message.Message):
    __slots__ = ("course_id",)
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    def __init__(self, course_id: _Optional[str] = ...) -> None: ...

class QuizData(_message.Message):
    __slots__ = ("id", "course_id", "section_id", "title", "description", "time_limit", "passing_score", "questions", "created_at", "updated_at", "deleted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    TIME_LIMIT_FIELD_NUMBER: _ClassVar[int]
    PASSING_SCORE_FIELD_NUMBER: _ClassVar[int]
    QUESTIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    course_id: str
    section_id: str
    title: str
    description: str
    time_limit: int
    passing_score: int
    questions: _containers.RepeatedCompositeFieldContainer[Question]
    created_at: str
    updated_at: str
    deleted_at: str
    def __init__(self, id: _Optional[str] = ..., course_id: _Optional[str] = ..., section_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., time_limit: _Optional[int] = ..., passing_score: _Optional[int] = ..., questions: _Optional[_Iterable[_Union[Question, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ...) -> None: ...

class QuizResponse(_message.Message):
    __slots__ = ("quiz", "error")
    QUIZ_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    quiz: QuizData
    error: _common_pb2.Error
    def __init__(self, quiz: _Optional[_Union[QuizData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class QuizzesData(_message.Message):
    __slots__ = ("quizzes",)
    QUIZZES_FIELD_NUMBER: _ClassVar[int]
    quizzes: _containers.RepeatedCompositeFieldContainer[QuizData]
    def __init__(self, quizzes: _Optional[_Iterable[_Union[QuizData, _Mapping]]] = ...) -> None: ...

class QuizzesResponse(_message.Message):
    __slots__ = ("quizzes", "error")
    QUIZZES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    quizzes: QuizzesData
    error: _common_pb2.Error
    def __init__(self, quizzes: _Optional[_Union[QuizzesData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteQuizResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
