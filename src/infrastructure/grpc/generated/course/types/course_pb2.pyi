from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from course.types import section_pb2 as _section_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CourseFilters(_message.Message):
    __slots__ = ("search", "category", "level", "minPrice", "maxPrice", "rating", "status")
    SEARCH_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MINPRICE_FIELD_NUMBER: _ClassVar[int]
    MAXPRICE_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    search: str
    category: _containers.RepeatedScalarFieldContainer[str]
    level: _containers.RepeatedScalarFieldContainer[str]
    minPrice: int
    maxPrice: int
    rating: int
    status: str
    def __init__(self, search: _Optional[str] = ..., category: _Optional[_Iterable[str]] = ..., level: _Optional[_Iterable[str]] = ..., minPrice: _Optional[int] = ..., maxPrice: _Optional[int] = ..., rating: _Optional[int] = ..., status: _Optional[str] = ...) -> None: ...

class GetCoursesParams(_message.Message):
    __slots__ = ("pagination", "filters")
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    pagination: _common_pb2.Pagination
    filters: CourseFilters
    def __init__(self, pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ..., filters: _Optional[_Union[CourseFilters, _Mapping]] = ...) -> None: ...

class GetCoursesRequest(_message.Message):
    __slots__ = ("params",)
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    params: GetCoursesParams
    def __init__(self, params: _Optional[_Union[GetCoursesParams, _Mapping]] = ...) -> None: ...

class CreateCourseRequest(_message.Message):
    __slots__ = ("title", "topics", "instructor_id", "instructor", "sub_title", "category", "sub_category", "language", "level", "subtitle_language", "duration_value", "duration_unit")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_ID_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SUB_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNIT_FIELD_NUMBER: _ClassVar[int]
    title: str
    topics: _containers.RepeatedScalarFieldContainer[str]
    instructor_id: str
    instructor: _common_pb2.User
    sub_title: str
    category: str
    sub_category: str
    language: str
    level: str
    subtitle_language: str
    duration_value: str
    duration_unit: str
    def __init__(self, title: _Optional[str] = ..., topics: _Optional[_Iterable[str]] = ..., instructor_id: _Optional[str] = ..., instructor: _Optional[_Union[_common_pb2.User, _Mapping]] = ..., sub_title: _Optional[str] = ..., category: _Optional[str] = ..., sub_category: _Optional[str] = ..., language: _Optional[str] = ..., level: _Optional[str] = ..., subtitle_language: _Optional[str] = ..., duration_value: _Optional[str] = ..., duration_unit: _Optional[str] = ...) -> None: ...

class GetCourseRequest(_message.Message):
    __slots__ = ("course_id",)
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    def __init__(self, course_id: _Optional[str] = ...) -> None: ...

class GetCoursesByIdsRequest(_message.Message):
    __slots__ = ("course_ids",)
    COURSE_IDS_FIELD_NUMBER: _ClassVar[int]
    course_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, course_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetCoursesByIdsResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: CoursesListResponse
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[CoursesListResponse, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class GetCourseBySlugRequest(_message.Message):
    __slots__ = ("slug",)
    SLUG_FIELD_NUMBER: _ClassVar[int]
    slug: str
    def __init__(self, slug: _Optional[str] = ...) -> None: ...

class UpdateCourseRequest(_message.Message):
    __slots__ = ("title", "topics", "sub_title", "category", "sub_category", "language", "level", "subtitle_language", "duration_value", "duration_unit", "course_id", "user_id", "description", "learning_outcomes", "target_audience", "requirements", "thumbnail", "trailer", "price", "discount_price", "currency")
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SUB_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNIT_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LEARNING_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TARGET_AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    TRAILER_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    title: str
    topics: _containers.RepeatedScalarFieldContainer[str]
    sub_title: str
    category: str
    sub_category: str
    language: str
    level: str
    subtitle_language: str
    duration_value: str
    duration_unit: str
    course_id: str
    user_id: str
    description: str
    learning_outcomes: _containers.RepeatedScalarFieldContainer[str]
    target_audience: _containers.RepeatedScalarFieldContainer[str]
    requirements: _containers.RepeatedScalarFieldContainer[str]
    thumbnail: str
    trailer: str
    price: int
    discount_price: int
    currency: str
    def __init__(self, title: _Optional[str] = ..., topics: _Optional[_Iterable[str]] = ..., sub_title: _Optional[str] = ..., category: _Optional[str] = ..., sub_category: _Optional[str] = ..., language: _Optional[str] = ..., level: _Optional[str] = ..., subtitle_language: _Optional[str] = ..., duration_value: _Optional[str] = ..., duration_unit: _Optional[str] = ..., course_id: _Optional[str] = ..., user_id: _Optional[str] = ..., description: _Optional[str] = ..., learning_outcomes: _Optional[_Iterable[str]] = ..., target_audience: _Optional[_Iterable[str]] = ..., requirements: _Optional[_Iterable[str]] = ..., thumbnail: _Optional[str] = ..., trailer: _Optional[str] = ..., price: _Optional[int] = ..., discount_price: _Optional[int] = ..., currency: _Optional[str] = ...) -> None: ...

class DeleteCourseRequest(_message.Message):
    __slots__ = ("course_id", "user_id")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    user_id: str
    def __init__(self, course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class UnPublishCourseRequest(_message.Message):
    __slots__ = ("course_id", "user_id")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    user_id: str
    def __init__(self, course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class PublishCourseRequest(_message.Message):
    __slots__ = ("course_id", "user_id")
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    course_id: str
    user_id: str
    def __init__(self, course_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetCoursesByInstructorRequest(_message.Message):
    __slots__ = ("instructor_id", "pagination")
    INSTRUCTOR_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    instructor_id: str
    pagination: _common_pb2.Pagination
    def __init__(self, instructor_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ...) -> None: ...

class GetEnrolledCoursesRequest(_message.Message):
    __slots__ = ("user_id", "pagination")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    pagination: _common_pb2.Pagination
    def __init__(self, user_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ...) -> None: ...

class CourseData(_message.Message):
    __slots__ = ("id", "title", "topics", "instructor_id", "sub_title", "category", "sub_category", "language", "subtitle_language", "level", "duration_value", "duration_unit", "description", "learning_outcomes", "target_audience", "requirements", "thumbnail", "trailer", "status", "slug", "rating", "number_of_rating", "students", "sections", "created_at", "updated_at", "deleted_at", "price", "discount_price", "currency", "instructor")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_ID_FIELD_NUMBER: _ClassVar[int]
    SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SUB_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNIT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LEARNING_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TARGET_AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    TRAILER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_RATING_FIELD_NUMBER: _ClassVar[int]
    STUDENTS_FIELD_NUMBER: _ClassVar[int]
    SECTIONS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    topics: _containers.RepeatedScalarFieldContainer[str]
    instructor_id: str
    sub_title: str
    category: str
    sub_category: str
    language: str
    subtitle_language: str
    level: str
    duration_value: str
    duration_unit: str
    description: str
    learning_outcomes: _containers.RepeatedScalarFieldContainer[str]
    target_audience: _containers.RepeatedScalarFieldContainer[str]
    requirements: _containers.RepeatedScalarFieldContainer[str]
    thumbnail: str
    trailer: str
    status: str
    slug: str
    rating: int
    number_of_rating: int
    students: int
    sections: _containers.RepeatedCompositeFieldContainer[_section_pb2.SectionData]
    created_at: str
    updated_at: str
    deleted_at: str
    price: int
    discount_price: int
    currency: str
    instructor: _common_pb2.User
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., topics: _Optional[_Iterable[str]] = ..., instructor_id: _Optional[str] = ..., sub_title: _Optional[str] = ..., category: _Optional[str] = ..., sub_category: _Optional[str] = ..., language: _Optional[str] = ..., subtitle_language: _Optional[str] = ..., level: _Optional[str] = ..., duration_value: _Optional[str] = ..., duration_unit: _Optional[str] = ..., description: _Optional[str] = ..., learning_outcomes: _Optional[_Iterable[str]] = ..., target_audience: _Optional[_Iterable[str]] = ..., requirements: _Optional[_Iterable[str]] = ..., thumbnail: _Optional[str] = ..., trailer: _Optional[str] = ..., status: _Optional[str] = ..., slug: _Optional[str] = ..., rating: _Optional[int] = ..., number_of_rating: _Optional[int] = ..., students: _Optional[int] = ..., sections: _Optional[_Iterable[_Union[_section_pb2.SectionData, _Mapping]]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., price: _Optional[int] = ..., discount_price: _Optional[int] = ..., currency: _Optional[str] = ..., instructor: _Optional[_Union[_common_pb2.User, _Mapping]] = ...) -> None: ...

class CourseMetadata(_message.Message):
    __slots__ = ("id", "title", "topics", "instructor_id", "sub_title", "category", "sub_category", "language", "subtitle_language", "level", "duration_value", "duration_unit", "description", "learning_outcomes", "target_audience", "requirements", "thumbnail", "trailer", "status", "slug", "rating", "number_of_rating", "students", "created_at", "updated_at", "deleted_at", "price", "no_of_lessons", "no_of_sections", "no_of_quizzes", "discount_price", "currency", "instructor")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    TOPICS_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_ID_FIELD_NUMBER: _ClassVar[int]
    SUB_TITLE_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    SUB_CATEGORY_FIELD_NUMBER: _ClassVar[int]
    LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    SUBTITLE_LANGUAGE_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    DURATION_VALUE_FIELD_NUMBER: _ClassVar[int]
    DURATION_UNIT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LEARNING_OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TARGET_AUDIENCE_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    TRAILER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SLUG_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    NUMBER_OF_RATING_FIELD_NUMBER: _ClassVar[int]
    STUDENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    DELETED_AT_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    NO_OF_LESSONS_FIELD_NUMBER: _ClassVar[int]
    NO_OF_SECTIONS_FIELD_NUMBER: _ClassVar[int]
    NO_OF_QUIZZES_FIELD_NUMBER: _ClassVar[int]
    DISCOUNT_PRICE_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    INSTRUCTOR_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    topics: _containers.RepeatedScalarFieldContainer[str]
    instructor_id: str
    sub_title: str
    category: str
    sub_category: str
    language: str
    subtitle_language: str
    level: str
    duration_value: str
    duration_unit: str
    description: str
    learning_outcomes: _containers.RepeatedScalarFieldContainer[str]
    target_audience: _containers.RepeatedScalarFieldContainer[str]
    requirements: _containers.RepeatedScalarFieldContainer[str]
    thumbnail: str
    trailer: str
    status: str
    slug: str
    rating: int
    number_of_rating: int
    students: int
    created_at: str
    updated_at: str
    deleted_at: str
    price: int
    no_of_lessons: int
    no_of_sections: int
    no_of_quizzes: int
    discount_price: int
    currency: str
    instructor: _common_pb2.User
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., topics: _Optional[_Iterable[str]] = ..., instructor_id: _Optional[str] = ..., sub_title: _Optional[str] = ..., category: _Optional[str] = ..., sub_category: _Optional[str] = ..., language: _Optional[str] = ..., subtitle_language: _Optional[str] = ..., level: _Optional[str] = ..., duration_value: _Optional[str] = ..., duration_unit: _Optional[str] = ..., description: _Optional[str] = ..., learning_outcomes: _Optional[_Iterable[str]] = ..., target_audience: _Optional[_Iterable[str]] = ..., requirements: _Optional[_Iterable[str]] = ..., thumbnail: _Optional[str] = ..., trailer: _Optional[str] = ..., status: _Optional[str] = ..., slug: _Optional[str] = ..., rating: _Optional[int] = ..., number_of_rating: _Optional[int] = ..., students: _Optional[int] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., deleted_at: _Optional[str] = ..., price: _Optional[int] = ..., no_of_lessons: _Optional[int] = ..., no_of_sections: _Optional[int] = ..., no_of_quizzes: _Optional[int] = ..., discount_price: _Optional[int] = ..., currency: _Optional[str] = ..., instructor: _Optional[_Union[_common_pb2.User, _Mapping]] = ...) -> None: ...

class CourseResponse(_message.Message):
    __slots__ = ("course", "error")
    COURSE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    course: CourseData
    error: _common_pb2.Error
    def __init__(self, course: _Optional[_Union[CourseData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class CoursesData(_message.Message):
    __slots__ = ("courses", "total")
    COURSES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[CourseData]
    total: int
    def __init__(self, courses: _Optional[_Iterable[_Union[CourseData, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class CoursesListData(_message.Message):
    __slots__ = ("courses", "total")
    COURSES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    courses: _containers.RepeatedCompositeFieldContainer[CourseMetadata]
    total: int
    def __init__(self, courses: _Optional[_Iterable[_Union[CourseMetadata, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class CoursesResponse(_message.Message):
    __slots__ = ("courses", "error")
    COURSES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    courses: CoursesData
    error: _common_pb2.Error
    def __init__(self, courses: _Optional[_Union[CoursesData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class CoursesListResponse(_message.Message):
    __slots__ = ("courses", "error")
    COURSES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    courses: CoursesListData
    error: _common_pb2.Error
    def __init__(self, courses: _Optional[_Union[CoursesListData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class DeleteCourseResponse(_message.Message):
    __slots__ = ("success", "error")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    success: _common_pb2.DeleteSuccess
    error: _common_pb2.Error
    def __init__(self, success: _Optional[_Union[_common_pb2.DeleteSuccess, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
