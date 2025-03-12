import logging
from datetime import datetime
from typing import List, Optional, Sequence, Type, Union
from uuid import uuid4

from django.db.models.query import QuerySet
from django.http import HttpResponseBase  # type: ignore
from rest_framework import pagination, viewsets
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, BaseThrottle

from ..get_throttle_details import get_throttle_details
from ..page_number_pagination import PageNumberPagination
from ..add_throttle_headers import add_throttle_headers

logger = logging.getLogger(__name__)


class BaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """ModelViewSet to provide standard response formatting and error handling."""

    filter_backends: List[Type[BaseFilterBackend]] = []
    lookup_field: str = "pk"
    lookup_url_kwarg: Optional[str] = None
    pagination_class: Optional[Type[pagination.PageNumberPagination]] = (
        PageNumberPagination
    )
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    queryset: QuerySet = QuerySet()
    search_fields: Optional[Sequence[str]] = ()
    throttle_classes: List[Type[BaseThrottle]] = [AnonRateThrottle]

    def finalize_response(
        self,
        request: Request,
        response: Union[Response, HttpResponseBase],
        *args,
        **kwargs,
    ) -> Union[Response, HttpResponseBase]:
        """Finalizes API response format with standard structure."""
        request_id = str(uuid4())
        throttles = get_throttle_details(self)
        data = getattr(response, "data", {})

        # Default response structure
        payload = {
            "status": "succeeded" if response.status_code < 400 else "failed",
            "status_code": response.status_code,
            "message": "",
            "data": {},
            "errors": [],
            "meta": {
                "response_time": "N/A",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "documentation_url": "https://github.com/shaileshpandit141/django-react-typescript-initial-code/tree/main",
                "rate_limits": throttles,
            },
        }

        if response.status_code >= 400:
            self._handle_error_response(response, data, payload)
        else:
            self._handle_success_response(response, request, data, payload)

        setattr(response, "data", payload)
        add_throttle_headers(response, throttles)
        self._set_custom_headers(response, request_id)

        logger.info(
            f"Response finalized with status {response.status_code}, Request ID: {request_id}"
        )
        return super().finalize_response(request, response, *args, **kwargs)

    def _handle_error_response(
        self, response: Union[Response, HttpResponseBase], data: dict, payload: dict
    ) -> None:
        """Handles error responses."""
        if response.status_code == 404:
            payload.update(
                {
                    "message": data.get("message", "Resource Not Found"),
                    "data": data.get("data", {}),
                    "errors": data.get(
                        "errors",
                        [
                            {
                                "field": "none",
                                "code": "not_found",
                                "message": "The requested resource was not found",
                                "details": {},
                            }
                        ],
                    ),
                }
            )
        else:
            payload.update(
                {
                    "message": data.get("message", "An unexpected error occurred."),
                    "data": data.get("data", {}),
                    "errors": data.get("errors", []),
                }
            )

    def _handle_success_response(
        self,
        response: Union[Response, HttpResponseBase],
        request: Request,
        data: dict,
        payload: dict,
    ) -> None:
        """Handles successful responses."""
        if response.status_code == 204:
            response.status_code = 200
            payload.update(
                {
                    "message": "The request was successful",
                    "data": {
                        "detail": "The requested resource deletion was successful.",
                        "id": getattr(request, "parser_context", {})
                        .setdefault("kwargs", {})
                        .get("pk", None),
                    },
                }
            )
        else:
            payload.update(
                {
                    "message": "The request was successful",
                    "data": data,
                }
            )

    def _set_custom_headers(
        self, response: Union[Response, HttpResponseBase], request_id: str
    ) -> None:
        """Sets custom headers for tracking request metadata."""
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
