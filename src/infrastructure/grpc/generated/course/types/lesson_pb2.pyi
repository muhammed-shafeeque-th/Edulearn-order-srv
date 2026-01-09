from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateLessonRequest(_message.Message):
    __slots__ = ("section_id", "course_id", "user_id", "is_preview", "description", "estimated_duration", "order", "title", "is_published", "content_type", "content_url", "metadata")
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_DURATION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_URL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    section_id: str
    course_id: str
    user_id: str
    is_preview: bool
    description: str
    estimated_duration: int
    order: int
    title: str
    is_published: bool
    content_type: str
    content_url: str
    metadata: ContentMetaData
    def __init__(self, section_id: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ..., is_preview: bool = ..., description: _Optional[str] = ..., estimated_duration: _Optional[int] = ..., order: _Optional[int] = ..., title: _Optional[str] = ..., is_published: bool = ..., content_type: _Optional[str] = ..., content_url: _Optional[str] = ..., metadata: _Optional[_Union[ContentMetaData, _Mapping]] = ...) -> None: ...

class GetLessonRequest(_message.Message):
    __slots__ = ("lesson_id",)
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    lesson_id: str
    def __init__(self, lesson_id: _Optional[str] = ...) -> None: ...

class UpdateLessonRequest(_message.Message):
    __slots__ = ("lesson_id", "course_id", "user_id", "section_id", "is_preview", "description", "estimated_duration", "order", "title", "is_published", "content_type", "content_url", "metadata")
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_DURATION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_URL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    lesson_id: str
    course_id: str
    user_id: str
    section_id: str
    is_preview: bool
    description: str
    estimated_duration: int
    order: int
    title: str
    is_published: bool
    content_type: str
    content_url: str
    metadata: ContentMetaData
    def __init__(self, lesson_id: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ..., section_id: _Optional[str] = ..., is_preview: bool = ..., description: _Optional[str] = ..., estimated_duration: _Optional[int] = ..., order: _Optional[int] = ..., title: _Optional[str] = ..., is_published: bool = ..., content_type: _Optional[str] = ..., content_url: _Optional[str] = ..., metadata: _Optional[_Union[ContentMetaData, _Mapping]] = ...) -> None: ...

class ContentMetaData(_message.Message):
    __slots__ = ("title", "file_name", "mime_type", "file_size", "url")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    title: str
    file_name: str
    mime_type: str
    file_size: str
    url: str
    def __init__(self, title: _Optional[str] = ..., file_name: _Optional[str] = ..., mime_type: _Optional[str] = ..., file_size: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class DeleteLessonRequest(_message.Message):
    __slots__ = ("lesson_id", "course_id", "user_id")
    LESSON_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    lesson_id: str
    course_id: str
    user_id: str
    def __init__(self, lesson_id: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetLessonsBySectionRequest(_message.Message):
    __slots__ = ("section_id",)
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    section_id: str
    def __init__(self, section_id: _Optional[str] = ...) -> None: ...

class LessonData(_message.Message):
    __slots__ = ("id", "section_id", "is_preview", "description", "estimated_duration", "order", "title", "is_published", "content_type", "content_url", "metadata", "created_at", "updated_at", "deleted_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    SECTION_ID_FIELD_NUMBER: _ClassVar[int]
    IS_PREVIEW_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ESTIMATED_DURATION_FIELD_NUMBER: _ClassVar[int]
    ORDER_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    IS_PUBLISHED_FIELD_NUMBER: _ClassVar[int]
    CONTENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_URL_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    section_id: str
    is_preview: bool
    description: str
    estimated_duration: int
    order: int
    title: str
    is_published: bool
    content_type: str
    content_url: str
    metadata: ContentMetaData
    created_at: str
    updated_at: str
    deleted_at: str
    def __init__(self, id: _Optional[str] = ..., section_id: _Optional[str] = ..., is_preview: bool = ..., description: _Optional[str] = ..., estimated_duration: _Optional[int] = ..., order: _Optional[int] = ..., title: _Optional[str] = ..., is_published: bool = ..., content_type: _Optional[str] = ..., content_url: _Optional[str] = ..., metadata: _Optional[_Union[ContentMetaData, _Mapping]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ...) -> None: ...

class LessonResponse(_message.Message):
    __slots__ = ("lesson", "error")
    LESSON_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    lesson: LessonData
    error: _common_pb2.Error
    def __init__(self, lesson: _Optional[_Union[LessonData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class LessonsData(_message.Message):
    __slots__ = ("lessons",)
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    lessons: _containers.RepeatedCompositeFieldContainer[LessonData]
    def __init__(self, lessons: _Optional[_Iterable[_Union[LessonData, _Mapping]]] = ...) -> None: ...

class LessonsResponse(_message.Message):
    __slots__ = ("lessons", "error")
    LESSONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    lessons: LessonsData
    error: _common_pb2.Error
    def __init__(self, lessons: _Optional[_Union[LessonsData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteLessonResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
