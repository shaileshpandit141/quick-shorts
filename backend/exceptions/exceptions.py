from core.response import Response
from rest_framework import status, views
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    Throttled,
    ValidationError,
    APIException,
)
from core.validation_error_formatter import ValidationErrorFormatter
from .create_error_response import create_error_response


def exception_handler(exc, context) -> Response | views.Response | None:
    """A custom exception handler that returns the exception details in a custom format."""
    response = views.exception_handler(exc, context)

    error_handlers = {
        ValidationError: lambda error: Response(
            {
                "message": "Validation error",
                "data": {},
                "errors": ValidationErrorFormatter.format(error.detail),
            },
            status=status.HTTP_400_BAD_REQUEST,
        ),
        MethodNotAllowed: lambda error: create_error_response(
            "Method Not Allowed",
            "method_not_allowed",
            error_message=getattr(
                error, "detail", "This method is not allowed for this endpoint."
            ),
        ),
        NotFound: lambda error: create_error_response(
            "Resource Not Found",
            "not_found",
            error_message=getattr(
                error, "detail", "The requested resource was not found."
            ),
        ),
        NotAuthenticated: lambda error: create_error_response(
            "Authentication Required",
            "authentication_required",
            error_message=getattr(
                error, "detail", "Authentication credentials were not provided."
            ),
        ),
        AuthenticationFailed: lambda error: create_error_response(
            "Authentication Failed",
            "authentication_failed",
            error_message=getattr(
                error, "detail", "Authentication credentials are incorrect."
            ),
        ),
        Throttled: lambda error: create_error_response(
            str(error.detail) or "Request Limit Exceeded",
            "throttled",
            error_message=getattr(
                error,
                "detail",
                "Allowed limit requests exceeded. Please try again later.",
            ),
            details={"retry_after": f"{error.wait} seconds"},
        ),
        APIException: lambda error: create_error_response(
            "An internal server error occurred.",
            "api_exception",
            error_message=getattr(error, "detail", "An unexpected error occurred."),
        ),
    }

    for exception_class, handler in error_handlers.items():
        if isinstance(exc, exception_class):
            response = handler(exc)
            if isinstance(exc, MethodNotAllowed):
                response.status_code = status.HTTP_405_METHOD_NOT_ALLOWED
            elif isinstance(exc, NotFound):
                response.status_code = status.HTTP_404_NOT_FOUND
            elif isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
                response.status_code = status.HTTP_401_UNAUTHORIZED
            elif isinstance(exc, Throttled):
                response.status_code = status.HTTP_429_TOO_MANY_REQUESTS
            elif isinstance(exc, APIException):
                response.status_code = getattr(
                    exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif isinstance(exc, Exception):
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

    return response
