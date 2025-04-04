from datetime import datetime

import pytz
from django.core.cache import cache
from rest_framework import status, views
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

from core.response import Response

from .create_error_response import create_error_response


def exception_handler(exc, context) -> Response | views.Response | None:
    """A custom exception handler that returns the exception details in a custom format."""
    response = views.exception_handler(exc, context)
    request = context.get("request", None)

    error_handlers = {
        ValidationError: lambda error: create_error_response(
            message="Validation error occurred. Please check your input.",
            errors=error,
            status=status.HTTP_400_BAD_REQUEST,
        ),
        MethodNotAllowed: lambda error: create_error_response(
            message="This HTTP method is not allowed for this endpoint.",
            errors=error,
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
        NotFound: lambda error: create_error_response(
            message="The requested resource could not be found.",
            errors=error,
            status=status.HTTP_404_NOT_FOUND,
        ),
        NotAuthenticated: lambda error: create_error_response(
            message="Please sign in to access this resource.",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        AuthenticationFailed: lambda error: create_error_response(
            message="Invalid credentials provided. Please check and try again.",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        Throttled: lambda error: create_error_response(
            message="Request limit exceeded. Please try again later.",
            errors=error,
            status=status.HTTP_429_TOO_MANY_REQUESTS,
        ),
        InvalidToken: lambda error: create_error_response(
            message="Your authentication token is invalid or has expired.",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        TokenError: lambda error: create_error_response(
            message="Authentication token error. Please provide a valid token.",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        APIException: lambda error: create_error_response(
            message="An unexpected error occurred. Our team has been notified.",
            errors=error,
        ),
        PermissionDenied: lambda error: create_error_response(
            message="Access denied - insufficient privileges.",
            errors=error,
        ),
    }

    # Handle all exceptions
    for exception_class, handler in error_handlers.items():
        if isinstance(exc, exception_class):
            response = handler(exc)
            if isinstance(exc, APIException):
                response.status_code = getattr(
                    exc, "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            elif isinstance(exc, Exception):
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            # Apply throttling if any exception is raised
            if request is not None:
                # Get the view (if available)
                view = context.get("view", None)

                is_authenticated = request.user.is_authenticated
                if is_authenticated:
                    # Use view-defined throttle classes or fallback to AnonRateThrottle
                    throttle_classes = getattr(view, "throttle_classes", None) or [
                        AnonRateThrottle
                    ]
                else:
                    throttle_classes = [AnonRateThrottle]
                    setattr(view, "throttle_classes", throttle_classes)

                # Iterate over the list of throttles class
                for throttle_class in throttle_classes:
                    throttle = throttle_class()  # Instantiate the throttle class
                    cache_key = throttle.get_cache_key(request, view)

                    if cache_key:
                        history = cache.get(cache_key, [])
                        now = datetime.now(pytz.UTC).timestamp()

                        # Remove expired requests from history
                        history = [
                            timestamp
                            for timestamp in history
                            if now - timestamp < throttle.duration
                        ]

                        # Check if throttle limit is exceeded or not
                        if isinstance(throttle.num_requests, int):
                            if len(history) >= throttle.num_requests:
                                retry_after = throttle.duration
                                if history:
                                    retry_after = int(
                                        throttle.duration - (now - history[0])
                                    )

                                return create_error_response(
                                    message="Rate limit exceeded",
                                    errors={
                                        "detail": "You have exceeded the rate limit. Please wait before making more requests.",
                                        "retry_after": f"{retry_after} seconds",
                                    },
                                    status=status.HTTP_429_TOO_MANY_REQUESTS,
                                )

                        # Otherwise, add the current request to history and update cache
                        history.append(now)
                        cache.set(cache_key, history, throttle.duration)

            # Return updaed response instance
            return response

    # Return un updaed response instance
    return response
