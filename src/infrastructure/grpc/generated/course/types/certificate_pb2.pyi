from src.infrastructure.grpc.generated.course import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CertificateData(_message.Message):
    __slots__ = ("id", "enrollment_id", "user_id", "course_id", "course_title", "student_name", "completed_at", "certificate_number", "issue_date", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_ID_FIELD_NUMBER: _ClassVar[int]
    COURSE_TITLE_FIELD_NUMBER: _ClassVar[int]
    STUDENT_NAME_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    ISSUE_DATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    enrollment_id: str
    user_id: str
    course_id: str
    course_title: str
    student_name: str
    completed_at: str
    certificate_number: str
    issue_date: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., course_id: _Optional[str] = ..., course_title: _Optional[str] = ..., student_name: _Optional[str] = ..., completed_at: _Optional[str] = ..., certificate_number: _Optional[str] = ..., issue_date: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class GetCertificateRequest(_message.Message):
    __slots__ = ("certificate_id", "user_id")
    CERTIFICATE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    certificate_id: str
    user_id: str
    def __init__(self, certificate_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetCertificateByEnrollmentRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GenerateCertificateRequest(_message.Message):
    __slots__ = ("enrollment_id", "user_id", "student_name")
    ENROLLMENT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    STUDENT_NAME_FIELD_NUMBER: _ClassVar[int]
    enrollment_id: str
    user_id: str
    student_name: str
    def __init__(self, enrollment_id: _Optional[str] = ..., user_id: _Optional[str] = ..., student_name: _Optional[str] = ...) -> None: ...

class DownloadCertificateRequest(_message.Message):
    __slots__ = ("certificate_id", "user_id")
    CERTIFICATE_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    certificate_id: str
    user_id: str
    def __init__(self, certificate_id: _Optional[str] = ..., user_id: _Optional[str] = ...) -> None: ...

class GetCertificatesByUserRequest(_message.Message):
    __slots__ = ("user_id", "pagination")
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    PAGINATION_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    pagination: _common_pb2.Pagination
    def __init__(self, user_id: _Optional[str] = ..., pagination: _Optional[_Union[_common_pb2.Pagination, _Mapping]] = ...) -> None: ...

class CertificatePDFChunk(_message.Message):
    __slots__ = ("data",)
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    def __init__(self, data: _Optional[bytes] = ...) -> None: ...

class CertificatesData(_message.Message):
    __slots__ = ("certificates", "total")
    CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    certificates: _containers.RepeatedCompositeFieldContainer[CertificateData]
    total: int
    def __init__(self, certificates: _Optional[_Iterable[_Union[CertificateData, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class CertificateResponse(_message.Message):
    __slots__ = ("certificate", "error")
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    certificate: CertificateData
    error: _common_pb2.Error
    def __init__(self, certificate: _Optional[_Union[CertificateData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...

class CertificatesResponse(_message.Message):
    __slots__ = ("certificates", "error")
    CERTIFICATES_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    certificates: CertificatesData
    error: _common_pb2.Error
    def __init__(self, certificates: _Optional[_Union[CertificatesData, _Mapping]] = ..., error: _Optional[_Union[_common_pb2.Error, _Mapping]] = ...) -> None: ...
