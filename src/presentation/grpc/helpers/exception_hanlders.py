from typing import Any
from grpc import aio

from src.infrastructure.grpc.generated.order_service_pb2 import Error, ErrorDetail


def create_error_response(code: str, message: str, details: list | None = None) -> Error:
        """Create a structured error response"""
        error_details = []
        if details:
            for detail in details:
                error_details.append(ErrorDetail(
                    field=detail.get('field', ''),
                    message=detail.get('message', '')
                ))

        return Error(
            code=code,
            message=message,
            details=error_details
        )
        
async def create_grpc_service_error(
    ctx: aio.ServicerContext,
    code: str,
    message: str,
    details: list | None = None
) -> None:
    """
    Create a structured gRPC service error using best practices:
    """
    import grpc
    import json

    # Prepare error details for metadata
    error_metadata = [
        ("error_code", code),
        ("message", message)
    ]
    if details is not None:
        try:
            # Serialize details as JSON string for transmission
            details_json = json.dumps(details)
            error_metadata.append(("details", details_json))
        except Exception:
            # Fallback: just pass string, but don't fail metadata
            error_metadata.append(("details", str(details)))

    # Map application error codes to gRPC StatusCode when possible, default to INTERNAL
    code_map = {
        "INVALID_ARGUMENT": grpc.StatusCode.INVALID_ARGUMENT,
        "NOT_FOUND": grpc.StatusCode.NOT_FOUND,
        "ALREADY_EXISTS": grpc.StatusCode.ALREADY_EXISTS,
        "PERMISSION_DENIED": grpc.StatusCode.PERMISSION_DENIED,
        "UNAUTHENTICATED": grpc.StatusCode.UNAUTHENTICATED,
        "FAILED_PRECONDITION": grpc.StatusCode.FAILED_PRECONDITION,
        "INTERNAL": grpc.StatusCode.INTERNAL,
    }
    grpc_code = code_map.get(code, grpc.StatusCode.INTERNAL)

    ctx.set_trailing_metadata(error_metadata)

    # Using ctx.abort will raise and propagate the gRPC error, do not return coroutine
    await ctx.abort(grpc_code, message)


def handle_grpc_exception(  exc: Exception, ctx: aio.ServicerContext, response_model: Any, operation: str = "operation", default_message: str = "Internal server error", logger=None):
        """
        Centralized gRPC exception handler for OrderServiceImpl.
        Handles (in order): RetryError (with DomainException chaining), DomainException, ValidationError, and generic Exception.
        """
        from tenacity import RetryError
        from src.domain.exceptions.exceptions import DomainException
        from pydantic import ValidationError

        import logging
        # Use the provided logger, or fall back to a module-level 'logger', or Python's root logger
        if logger is not None:
            log = logger
        elif 'logger' in globals() and hasattr(globals()['logger'], 'error'):
            log = globals()['logger']
        else:
            log = logging.getLogger("grpc.exception_handlers")

        if isinstance(exc, RetryError):
            actual_exception = exc.last_attempt.exception()
            if isinstance(actual_exception, DomainException):
                if log:
                    log.error(
                        f"RetryError caught with DomainException for {operation}: {actual_exception}")
                return response_model(
                    error=create_error_response(
                        code=type(actual_exception).__name__,
                        message=str(actual_exception),
                        details=[{"field": "request",
                                  "message": str(actual_exception)}]
                    )
                )
            else:
                if log:
                    log.error(f"RetryError in {operation}: {exc}")
                return response_model(
                    error=create_error_response(
                        code="INTERNAL",
                        message=default_message,
                        details=[{"field": "service", "message": str(exc)}]
                    )
                )
        elif isinstance(exc, DomainException):
            if log:
                log.error(f"DomainException in {operation}: {exc}")
            return response_model(
                error=create_error_response(
                    code=type(exc).__name__,
                    message=str(exc),
                    details=[{"field": "request", "message": str(exc)}]
                )
            )
        elif isinstance(exc, ValidationError):
            details = []
            for err in exc.errors():
                field_path = ".".join(str(p) for p in err.get("loc", []))
                details.append({
                    "field": field_path or "request",
                    "message": err.get("msg", "Invalid value"),
                })
            if log:
                log.error(f"Validation error in {operation}: {exc}")
            return response_model(
                error=create_error_response(
                    code="INVALID_ARGUMENT",
                    message="Invalid request data",
                    details=details,
                )
            )
        else:
            if log:
                log.error(f"Unhandled exception in {operation}: {exc}")
            return create_grpc_service_error(
                    ctx=ctx, 
                    code="INTERNAL",
                    message=default_message,
                    details=[{"field": "service", "message": str(exc)}]
                )