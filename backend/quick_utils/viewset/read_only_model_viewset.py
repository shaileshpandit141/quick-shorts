from typing import Dict, Any, List, Type, Optional, Sequence
import logging
from rest_framework.request import Request
from django.http import HttpResponseBase
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import BaseThrottle
from rest_framework.filters import BaseFilterBackend
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.renderers import BaseRenderer
from ..get_throttle_details import get_throttle_details
from ..page_number_pagination import PageNumberPagination


logger = logging.getLogger(__name__)


class ReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset that standardizes API response formatting and error handling."""

    authentication_classes: List[Type[BaseAuthentication]] = []
    filter_backends: List[Type[BaseFilterBackend]] = []
    lookup_field: str = 'pk'
    lookup_url_kwarg: Optional[str] = None
    pagination_class: Type[pagination.PageNumberPagination] = PageNumberPagination
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    renderer_classes: Optional[List[Type[BaseRenderer]]] = None
    search_fields: Optional[Sequence[str]] = None
    throttle_classes: List[Type[BaseThrottle]] = [AnonRateThrottle]

    def _create_error_dict(self, field: str, error: Any, code: str = "error") -> Dict[str, Any]:
        """Formats an error into a standardized dictionary format."""
        logger.debug(f"Creating error dict for field {field}: {error}")
        return {
            "field": field,
            "code": getattr(error, "code", code),
            "message": str(error),
            "details": getattr(error, "details", None)
        }

    def _process_field_errors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Converts validation errors into list of standardized error dictionaries."""
        logger.debug(f"Processing field errors: {data}")
        errors = []
        for field, error_list in data.items():
            if field == "detail":
                continue

            field = "none" if field == "non_field_errors" else field
            if isinstance(error_list, list):
                errors.extend(
                    [self._create_error_dict(field, error) for error in error_list]
                )
            else:
                errors.append(self._create_error_dict(field, error_list))

        return errors

    def _build_error_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates standardized error response with message and error details."""
        logger.error(f"Building error response for data: {data}")
        errors = self._process_field_errors(data)
        if "detail" in data:
            errors.append(self._create_error_dict("none", data["detail"]))

        return {
            "message": data.get("detail", "An error occurred"),
            "errors": errors
        }

    def _build_success_response(self, data: Any) -> Dict[str, Any]:
        """Creates standardized success response with data payload."""
        logger.info("Building success response")
        return {
            "message": "Request completed successfully",
            "data": data
        }

    def finalize_response(
        self,
        request: Request,
        response: Response | HttpResponseBase,
        *args,
        **kwargs
    ) -> Response | HttpResponseBase:
        """
        Processes response before returning to client.
        Adds standard formatting and throttling information.
        """
        data = getattr(response, "data", None)

        if response.status_code >= 400:
            logger.warning(f"Error response with status {response.status_code}")
            custom_response = self._build_error_response(data) if isinstance(data, dict) else {
                "message": "An error occurred",
                "errors": []
            }
        else:
            logger.info(f"Success response with status {response.status_code}")
            custom_response = self._build_success_response(data)

        setattr(response, "throttles", get_throttle_details(self))
        setattr(response, "data", custom_response)
        return super().finalize_response(request, response, *args, **kwargs)
