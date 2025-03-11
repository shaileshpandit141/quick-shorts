import logging
from typing import Any, Dict, List, Self, Type
from datetime import datetime
from uuid import uuid4
from django.db.models import QuerySet
from django.http.response import HttpResponseBase
from rest_framework import status
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.throttling import BaseThrottle
from rest_framework.views import APIView
from ..validation_error_formatter import ValidationErrorFormatter
from ..get_throttle_details import get_throttle_details
from ..add_throttle_headers import add_throttle_headers
from ..page_number_pagination import PageNumberPagination
from .types import (
    TypeData,
    TypeErrorPayload,
    TypeErrors,
    TypeResponsePayload,
    TypeSuccessPayload,
)

logger = logging.getLogger(__name__)


class BaseAPIResponseHandler:
    """
    A handler class for generating standardized API responses.

    Methods:
    --------
    response(payload: TypeResponsePayload, status: int = status.HTTP_200_OK, **kwargs: Any) -> Response:
        Generates a generic API response with the given payload and status.

    success(payload: TypeSuccessPayload, status: int = status.HTTP_200_OK, **kwargs: Any) -> Response:
        Generates a success API response with the given payload and status.

    error(payload: TypeErrorPayload, status: int = status.HTTP_500_INTERNAL_SERVER_ERROR, **kwargs: Any) -> Response:
        Generates an error API response with the given payload and status.
    """

    def response(
        self: Self,
        payload: TypeResponsePayload,
        status: int = status.HTTP_200_OK,
        **kwargs: Any,
    ) -> Response:
        logger.debug(
            f"Generating response with payload: {payload} and status: {status}"
        )

        errors = payload.get("errors", None)
        if errors is None:
            errors = []
        else:
            errors = [
                {**error, "details": error.get("details", None)}
                for error in payload["errors"]
            ]

        return Response(
            data={
                "message": payload["message"],
                "data": payload.get("data", {}),
                "errors": errors,
            },
            status=status,
            **kwargs,
        )

    def success(
        self: Self,
        payload: TypeSuccessPayload,
        status: int = status.HTTP_200_OK,
        **kwargs: Any,
    ) -> Response:
        logger.info(f"Success response with payload: {payload} and status: {status}")
        return self.response(
            payload={**payload, "errors": []},
            status=status,
            **kwargs,
        )

    def error(
        self: Self,
        payload: TypeErrorPayload,
        status: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        **kwargs: Any,
    ) -> Response:
        logger.error(f"Error response with payload: {payload} and status: {status}")
        return self.response(
            payload={
                "message": payload["message"],
                "data": {},
                "errors": payload["errors"],
            },
            status=status,
            **kwargs,
        )


class BaseAPIView(APIView, BaseAPIResponseHandler):
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    throttle_classes: List[Type[BaseThrottle]] = []
    pagination_class: Type[PageNumberPagination] = PageNumberPagination

    def __init__(self, *args, **kwargs) -> None:
        """Initialize view with status attribute"""
        self.status = status
        self.formatter = ValidationErrorFormatter()
        super().__init__(*args, **kwargs)

    def finalize_response(
        self, request, response, *args, **kwargs
    ) -> Response | HttpResponseBase:
        throttles = get_throttle_details(self)
        request_id = str(uuid4())
        payload = {
            "status": "succeeded" if response.status_code < 400 else "failed",
            "status_code": response.status_code,
            **response.data,
            "meta": {
                "response_time": "N/A",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "documentation_url": "https://github.com/shaileshpandit141/django-react-typescript-initial-code/tree/main",
                "rate_limits": throttles,
            },
        }
        # Update the response data.
        setattr(response, "data", payload)

        # Add throttles details in headers.
        add_throttle_headers(response, throttles)

        # Update response headers.
        setattr(
            response,
            "headers",
            {
                **response.headers,
                "X-Request-ID": request_id,
                "X-Status-Code": str(response.status_code),
                "X-Status-Message": (
                    "succeeded" if response.status_code < 400 else "failed"
                ),
            },
        )

        logger.info(
            f"Response finalized with status {response.status_code}, Request ID: {request_id}"
        )

        # Call to super methods to handle rest process.
        return super().finalize_response(request, response, *args, **kwargs)

    def handle_success(
        self, message: str, data: TypeData, status: int = status.HTTP_200_OK
    ) -> Response:
        logger.info(
            f"Handling success with message: {message}, data: {data}, status: {status}"
        )
        return self.success({"message": message, "data": data}, status=status)

    def handle_error(
        self,
        message: str,
        errors: TypeErrors,
        status: int = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        logger.warning(
            f"Handling error with message: {message}, errors: {errors}, status: {status}"
        )
        return self.error({"message": message, "errors": errors}, status=status)

    def get_object(self, model, *args, **kwargs) -> Dict[str, Any] | None:
        """Get single model instance or None if not found"""
        try:
            return model.objects.get(*args, **kwargs)
        except model.DoesNotExist:
            logger.info(
                f"Object not found for model {model.__name__} with args: {args}, kwargs: {kwargs}"
            )
            return None

    def get_paginated_data(self, queryset: QuerySet) -> Dict[str, Any] | QuerySet:
        """
        Returns pagination data for the given queryset.
        Uses page and items-per-page query params if not explicitly provided.
        Default page is 1, default items per page is 10.
        """
        paginator = self.pagination_class()

        # Paginate the queryset
        page = paginator.paginate_queryset(queryset, self.request)
        if page is not None:
            logger.debug("Returning paginated response")
            return {
                "current_page": paginator.page.number,
                "total_pages": paginator.page.paginator.num_pages,
                "total_items": paginator.page.paginator.count,
                "items_per_page": paginator.page.paginator.per_page,
                "has_next": paginator.page.has_next(),
                "has_previous": paginator.page.has_previous(),
                "next_page_number": (
                    paginator.page.next_page_number()
                    if paginator.page.has_next()
                    else None
                ),
                "previous_page_number": (
                    paginator.page.previous_page_number()
                    if paginator.page.has_previous()
                    else None
                ),
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": page,
            }

        # If no pagination is required
        logger.debug("Returning unpaginated response")
        return queryset
