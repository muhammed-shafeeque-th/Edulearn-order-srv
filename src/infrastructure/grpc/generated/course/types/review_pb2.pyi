from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmitCourseReviewRequest(_message.Message):
    __slots__ = ("rating", "comment", "enrollment_id", "user_id", "user")
    RATING_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    rating: int
    comment: str
    enrollment_id: str
    user_id: str
    user: _common_pb2.User
    def __init__(self, rating: _Optional[int] = ..., comment: _Optional[str] = ..., enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., user: _Optional[_Union[_common_pb2.User, _Mapping]] = ...) -> None: ...

class GetReviewRequest(_message.Message):
    __slots__ = ("review_id",)
    REVIEW_ID_FIELD_NUMBER: _ClassVar[int]
    review_id: str
    def __init__(self, review_id: _Optional[str] = ...) -> None: ...

class GetReviewByEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class UpdateReviewRequest(_message.Message):
    __slots__ = ("review_id", "user_id", "enrollment_id", "rating", "comment")
    REVIEW_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    review_id: str
    user_id: str
    enrollment_id: str
    rating: int
    comment: str
    def __init__(self, review_id: _Optional[str] = ..., user_id: _Optional[str] = ..., enrollment_id: _Optional[str] = ..., rating: _Optional[int] = ..., comment: _Optional[str] = ...) -> None: ...

class DeleteReviewRequest(_message.Message):
    __slots__ = ("review_id", "user_id", "enrollment_id")
    REVIEW_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    review_id: str
    user_id: str
    enrollment_id: str
    def __init__(self, review_id: _Optional[str] = ..., user_id: _Optional[str] = ..., enrollment_id: _Optional[str] = ...) -> None: ...

class GetReviewsByCourseRequest(_message.Message):
    __slots__ = ("course_id", "pagination")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    pagination: _common_pb2.Pagination
    def __init__(self, course_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ...) -> None: ...

class ReviewData(_message.Message):
    __slots__ = ("id", "user_id", "course_id", "enrollment_id", "rating", "comment", "created_at", "updated_at", "user")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    COMMENT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    course_id: str
    enrollment_id: str
    rating: int
    comment: str
    created_at: str
    updated_at: str
    user: _common_pb2.User
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., course_id: _Optional[str] = ..., enrollment_id: _Optional[str] = ..., rating: _Optional[int] = ..., comment: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., user: _Optional[_Union[_common_pb2.User, _Mapping]] = ...) -> None: ...

class ReviewResponse(_message.Message):
    __slots__ = ("review", "error")
    REVIEW_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    review: ReviewData
    error: _common_pb2.Error
    def __init__(self, review: _Optional[_Union[ReviewData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class ReviewsData(_message.Message):
    __slots__ = ("reviews", "total")
    REVIEWS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    reviews: _containers.RepeatedCompositeFieldContainer[ReviewData]
    total: int
    def __init__(self, reviews: _Optional[_Iterable[_Union[ReviewData, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class ReviewsResponse(_message.Message):
    __slots__ = ("reviews", "error")
    REVIEWS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    reviews: ReviewsData
    error: _common_pb2.Error
    def __init__(self, reviews: _Optional[_Union[ReviewsData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteReviewResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
