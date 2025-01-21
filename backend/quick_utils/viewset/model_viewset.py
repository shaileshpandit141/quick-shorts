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


class ModelViewSet(viewsets.ModelViewSet):
    """Extends ModelViewSet to provide standard response formatting and error handling."""

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
        """Creates standardized error dictionary with field, code, message and details."""
        error_dict = {
            "field": field,
            "code": getattr(error, "code", code),
            "message": str(error),
            "details": getattr(error, "details", None)
        }
        logger.error(f"API Error: {error_dict}")
        return error_dict

    def _process_field_errors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Converts API validation errors to standard format."""
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
        """Formats error response with message and error details."""
        errors = self._process_field_errors(data)
        if "detail" in data:
            errors.append(self._create_error_dict("none", data["detail"]))

        error_response = {
            "message": data.get("detail", "An error occurred"),
            "errors": errors
        }
        logger.error(f"Error Response: {error_response}")
        return error_response

    def _build_success_response(self, data: Any) -> Dict[str, Any]:
        """Formats successful response with message and data."""
        logger.info("Request completed successfully")
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
        """Finalizes API response format with standard structure and throttling info."""
        data = getattr(response, "data", None)

        if response.status_code >= 400:
            logger.error(f"Request failed with status code {response.status_code}")
            custom_response = self._build_error_response(data) if isinstance(data, dict) else {
                "message": "An error occurred",
                "errors": []
            }
        else:
            logger.info(f"Request succeeded with status code {response.status_code}")
            custom_response = self._build_success_response(data)

        setattr(response, "throttles", get_throttle_details(self))
        setattr(response, "data", custom_response)
        return super().finalize_response(request, response, *args, **kwargs)
