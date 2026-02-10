from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ("code", "message", "details")
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    code: str
    message: str
    details: _containers.RepeatedCompositeFieldContainer[ErrorDetail]
    def __init__(self, code: _Optional[str] = ..., message: _Optional[str] = ..., details: _Optional[_Iterable[_Union[ErrorDetail, _Mapping]]] = ...) -> None: ...

class ErrorDetail(_message.Message):
    __slots__ = ("field", "message")
    FIELD_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    field: str
    message: str
    def __init__(self, field: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "name", "avatar", "email")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AVATAR_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    avatar: str
    email: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., avatar: _Optional[str] = ..., email: _Optional[str] = ...) -> None: ...

class Pagination(_message.Message):
    __slots__ = ("page", "page_size", "sort_by", "sort_order")
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_SIZE_FIELD_NUMBER: _ClassVar[int]
    SORT_BY_FIELD_NUMBER: _ClassVar[int]
    SORT_ORDER_FIELD_NUMBER: _ClassVar[int]
    page: int
    page_size: int
    sort_by: str
    sort_order: str
    def __init__(self, page: _Optional[int] = ..., page_size: _Optional[int] = ..., sort_by: _Optional[str] = ..., sort_order: _Optional[str] = ...) -> None: ...

class DeleteSuccess(_message.Message):
    __slots__ = ("deleted",)
    DELETED_FIELD_NUMBER: _ClassVar[int]
    deleted: bool
    def __init__(self, deleted: bool = ...) -> None: ...
