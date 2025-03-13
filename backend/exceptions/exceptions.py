from core.response import Response
from rest_framework import status, views
from .create_error_response import create_error_response
from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    Throttled,
    ValidationError,
    APIException,
)


def exception_handler(exc, context) -> Response | views.Response | None:
    """A custom exception handler that returns the exception details in a custom format."""
    response = views.exception_handler(exc, context)

    error_handlers = {
        ValidationError: lambda error: create_error_response(
            message="Oops! validation error occurs",
            errors=error,
            status=status.HTTP_400_BAD_REQUEST,
        ),
        MethodNotAllowed: lambda error: create_error_response(
            message="Method not allowed on this endpoint",
            errors=error,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
        NotFound: lambda error: create_error_response(
            message="Resource not found with given credential",
            errors=error,
            status=status.HTTP_404_NOT_FOUND,
        ),
        NotAuthenticated: lambda error: create_error_response(
            message="Authentication required on this endpoint",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        AuthenticationFailed: lambda error: create_error_response(
            message="Authentication failed. Please try again later",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        Throttled: lambda error: create_error_response(
            message="Opps! request limit exceeded",
            errors=error,
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        ),
        APIException: lambda error: create_error_response(
            message="Something went wrong. Please try again later",
            errors=error,
        ),
    }

    for exception_class, handler in error_handlers.items():
        if isinstance(exc, exception_class):
            response = handler(exc)
            if isinstance(exc, APIException):
                response.status_code = getattr(
                    exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif isinstance(exc, Exception):
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return response

    return response
