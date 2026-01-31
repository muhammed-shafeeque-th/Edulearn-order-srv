from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from . import quiz_pb2 as _quiz_pb2
from . import lesson_pb2 as _lesson_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSectionRequest(_message.Message):
    __slots__ = ("course_id", "user_id", "title", "description", "order", "is_published")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    user_id: str
    title: str
    description: str
    order: int
    is_published: bool
    def __init__(self, course_id: _Optional[str] = ..., user_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., order: _Optional[int] = ..., is_published: bool = ...) -> None: ...

class GetSectionRequest(_message.Message):
    __slots__ = ("section_id",)
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    section_id: str
    def __init__(self, section_id: _Optional[str] = ...) -> None: ...

class UpdateSectionRequest(_message.Message):
    __slots__ = ("section_id", "user_id", "course_id", "title", "description", "is_published", "order")
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    section_id: str
    user_id: str
    course_id: str
    title: str
    description: str
    is_published: bool
    order: int
    def __init__(self, section_id: _Optional[str] = ..., user_id: _Optional[str] = ..., course_id: _Optional[str] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., is_published: bool = ..., order: _Optional[int] = ...) -> None: ...

class DeleteSectionRequest(_message.Message):
    __slots__ = ("section_id", "course_id", "user_id")
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    section_id: str
    course_id: str
    user_id: str
    def __init__(self, section_id: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetSectionsByCourseRequest(_message.Message):
    __slots__ = ("course_id",)
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    def __init__(self, course_id: _Optional[str] = ...) -> None: ...

class SectionData(_message.Message):
    __slots__ = ("id", "course_id", "title", "lessons", "created_at", "updated_at", "deleted_at", "description", "is_published", "order", "quiz")
    ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    QUIZ_FIELD_NUMBER: _ClassVar[int]
    id: str
    course_id: str
    title: str
    lessons: _containers.RepeatedCompositeFieldContainer[_lesson_pb2.LessonData]
    created_at: str
    updated_at: str
    deleted_at: str
    description: str
    is_published: bool
    order: int
    quiz: _quiz_pb2.QuizData
    def __init__(self, id: _Optional[str] = ..., course_id: _Optional[str] = ..., title: _Optional[str] = ..., lessons: _Optional[_Iterable[_Union[_lesson_pb2.LessonData, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., description: _Optional[str] = ..., is_published: bool = ..., order: _Optional[int] = ..., quiz: _Optional[_Union[_quiz_pb2.QuizData, _Mapping]] = ...) -> None: ...

class SectionResponse(_message.Message):
    __slots__ = ("section", "error")
    SECTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    section: SectionData
    error: _common_pb2.Error
    def __init__(self, section: _Optional[_Union[SectionData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class SectionsData(_message.Message):
    __slots__ = ("sections",)
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    sections: _containers.RepeatedCompositeFieldContainer[SectionData]
    def __init__(self, sections: _Optional[_Iterable[_Union[SectionData, _Mapping]]] = ...) -> None: ...

class SectionsResponse(_message.Message):
    __slots__ = ("sections", "error")
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    sections: SectionsData
    error: _common_pb2.Error
    def __init__(self, sections: _Optional[_Union[SectionsData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteSectionResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
