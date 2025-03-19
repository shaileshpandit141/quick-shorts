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

from ..page_number_pagination import PageNumberPagination
from ..throttle_inspector import ThrottleInspector
from .view_set_utils import ViewSetUtils

logger = logging.getLogger(__name__)


class BaseModelViewSet(viewsets.ModelViewSet, ViewSetUtils):
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
        # Initialize ThrottleInspector class
        throttle_inspector = ThrottleInspector(self)

        # Inspect the throttles details
        throttle_details = throttle_inspector.get_details()

        # Attach throttle details in headers
        throttle_inspector.attach_headers(response, throttle_details)

        # Generate the uuid4 token
        request_id = str(uuid4())

        data = getattr(response, "data", {})

        # Default response structure
        payload = {
            "status": "succeeded" if response.status_code < 400 else "failed",
            "status_code": response.status_code,
            "message": "",
            "data": {},
            "errors": {},
            "meta": {
                "response_time": "N/A",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "documentation_url": "https://github.com/shaileshpandit141/django-react-typescript-initial-code/tree/main",
                "rate_limits": throttle_details,
            },
        }

        if response.status_code >= 400:
            self._handle_error_response(response, data, payload)
        else:
            self._handle_success_response(response, request, data, payload)

        setattr(response, "data", payload)
        self._set_custom_headers(response, request_id)

        logger.info(
            f"Response finalized with status {response.status_code}, Request ID: {request_id}"
        )
        return super().finalize_response(request, response, *args, **kwargs)
