class DomainException(Exception):
    pass

class OrderNotFoundException(DomainException):
    pass

class UserNotFoundException(DomainException):
    pass

class CourseNotFoundException(DomainException):
    pass

class CourseAlreadyEnrolledException(DomainException):
    pass

class SessionNotFoundException(DomainException):
    pass

class ConcurrencyException(DomainException):
    pass

class SagaExecutionException(DomainException):
    pass