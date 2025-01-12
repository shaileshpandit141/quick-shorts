from rest_framework.views import exception_handler
from rest_framework.exceptions import (
    ValidationError,
    MethodNotAllowed,
    NotFound,
    NotAuthenticated,
    AuthenticationFailed
)
from quick_utils.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    A custom exception handler that returns the exception details in a custom format.
    """
    # Call the default exception handler first to get the standard DRF response
    response = exception_handler(exc, context)

    # Handle specific exceptions

    # ValidationError
    if isinstance(exc, ValidationError):
        error_details = []
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
            "status": "failed",
            "message": "Validation error",
            "data": None,
            "errors": error_details
        }, status=status.HTTP_400_BAD_REQUEST)

    # MethodNotAllowed
    elif isinstance(exc, MethodNotAllowed):
        return Response({
            "status": "failed",
            "message": "Method Not Allowed",
            "data": None,
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
            "status": "failed",
            "message": "Resource Not Found",
            "data": None,
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
            "status": "failed",
            "message": "Authentication Required",
            "data": None,
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
            "status": "failed",
            "message": "Authentication Failed",
            "data": None,
            "errors": [{
                "field": "none",
                "code": "authentication_failed",
                "message": "Authentication credentials are incorrect",
                "details": None
            }]
        }, status=status.HTTP_401_UNAUTHORIZED)

    # General Exception
    elif isinstance(exc, Exception):
        return Response({
            "status": "failed",
            "message": "Internal Server Error",
            "data": None,
            "errors": [{
                "field": "none",
                "code": "server_error",
                "message": str(exc),
                "details": None
            }]
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Return the default response if no specific handler is found
    return response
