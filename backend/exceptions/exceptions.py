from rest_framework.views import exception_handler as dj_exception_handler
from rest_framework.exceptions import (
    ValidationError,
    MethodNotAllowed,
    NotFound,
    NotAuthenticated,
    AuthenticationFailed,
    Throttled
)
from quick_utils.types import ErrorsType
from quick_utils.response import Response
from rest_framework import status


def exception_handler(exc, context):
    """A custom exception handler that returns the exception details in a custom format."""

    # Call the default exception handler first to get the standard DRF response
    response = dj_exception_handler(exc, context)

    # Handle specific exceptions

    # ValidationError
    if isinstance(exc, ValidationError):
        error_details: ErrorsType = []
        if isinstance(exc.detail, dict):
            for field, messages in exc.detail.items():
                if isinstance(messages, list):
                    for message in messages:
                        error_details.append({
                            "field": field,
                            "code": getattr(message, "code", "validation_error"),
                            "message": str(message),
                            "details": None
                        })
                else:
                    error_details.append({
                        "field": field,
                        "code": getattr(messages, "code", "validation_error"),
                        "message": str(messages),
                        "details": None
                    })
        else:
            error_details.append({
                "field": "none",
                "code": "validation_error",
                "message": str(exc.detail),
                "details": None
            })

        return Response({
            "message": "Validation error",
            "errors": error_details
        }, status=status.HTTP_400_BAD_REQUEST)

    # MethodNotAllowed
    elif isinstance(exc, MethodNotAllowed):
        return Response({
            "message": "Method Not Allowed",
            "errors": [{
                "field": "none",
                "code": "method_not_allowed",
                "message": "This method is not allowed for this endpoint",
                "details": None
            }]
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    # NotFound
    elif isinstance(exc, NotFound):
        return Response({
            "message": "Resource Not Found",
            "errors": [{
                "field": "none",
                "code": "not_found",
                "message": "The requested resource was not found",
                "details": None
            }]
        }, status=status.HTTP_404_NOT_FOUND)

    # NotAuthenticated
    elif isinstance(exc, NotAuthenticated):
        return Response({
            "message": "Authentication Required",
            "errors": [{
                "field": "none",
                "code": "authentication_required",
                "message": "Authentication credentials were not provided",
                "details": None
            }]
        }, status=status.HTTP_401_UNAUTHORIZED)

    # AuthenticationFailed
    elif isinstance(exc, AuthenticationFailed):
        return Response({
            "message": "Authentication Failed",
            "errors": [{
                "field": "none",
                "code": "authentication_failed",
                "message": "Authentication credentials are incorrect",
                "details": None
            }]
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Throttled 
    elif isinstance(exc, Throttled):
        retry_after = exc.wait
        return Response({
            "message": str(exc.detail) or "Request Limit Exceeded",
            "errors": [{
                "field": "none",
                "code": "throttled",
                "message": "Too many requests. Please try again later.",
                "details": {
                    "retry_after": f"{retry_after} seconds"
                }
            }]
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)

    # General Exception
    elif isinstance(exc, Exception):
        return Response({
            "message": "Internal Server Error",
            "errors": [{
                "field": "none",
                "code": "server_error",
                "message": exc[0] if isinstance(exc, list) else str(exc),
                "details": None
            }]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return the default response if no specific handler is found
    return response
