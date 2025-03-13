from datetime import datetime

import pytz
from core.response import Response
from django.core.cache import cache
from rest_framework import status, views
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    Throttled,
    ValidationError,
)
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from throttling import AnonRateThrottle

from .create_error_response import create_error_response


def exception_handler(exc, context) -> Response | views.Response | None:
    """A custom exception handler that returns the exception details in a custom format."""
    response = views.exception_handler(exc, context)
    request = context.get("request", None)

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
        InvalidToken: lambda error: create_error_response(
            message="Invalid token: token is invalid or expired",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        TokenError: lambda error: create_error_response(
            message="Token error: please provide a valid token",
            errors=error,
            status=status.HTTP_401_UNAUTHORIZED,
        ),
        APIException: lambda error: create_error_response(
            message="Something went wrong. Please try again later",
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
                                    message="Opps! request limit exceeded",
                                    errors={
                                        "detail": "Opps! request limit exceeded. Please try again later.",
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
