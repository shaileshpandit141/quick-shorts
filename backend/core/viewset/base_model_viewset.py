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


class BaseModelViewSet(viewsets.ModelViewSet):
    """ModelViewSet to provide standard response formatting and error handling."""

    # Default configurations
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
        throttles = get_throttle_details(self)
        request_id = str(uuid4())

        # Ensure response data exists
        data = getattr(response, "data", {})

        # Correctly detect validation errors
        if isinstance(data, dict) and "errors" in data:
            response.status_code = 400

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

        # Handle errors separately
        if response.status_code >= 400:
            if response.status_code == 404:
                payload.update({"message": data.get("message", "Resource Not Found")})
                payload.update({"data": data.get("data", {})})
                payload.update(
                    {
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
                        )
                    }
                )
            else:
                payload.update(
                    {"message": data.get("message", "An Unexpected error occured.")}
                )
                payload.update({"data": data.get("data", {})})
                payload.update({"errors": data.get("errors", [])})
        else:
            if response.status_code == 204:
                response.status_code = 200
                payload.update(
                    {
                        "message": "The request was successful",
                        "data": {
                            "deatil": "The requested resource deletion was successful.",
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
                        "data": response.data,
                    }
                )

        # Assign the updated payload
        setattr(response, "data", payload)

        # Add throttle details in headers
        add_throttle_headers(response, throttles)

        # Add custom headers
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

        # Call to super methods to handle rest process
        return super().finalize_response(request, response, *args, **kwargs)
