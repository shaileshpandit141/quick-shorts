from typing import Dict, Any, List, Type, Optional, Sequence, Union
import logging
from rest_framework.request import Request
from django.http import HttpResponseBase
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import pagination
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import BaseThrottle
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import BasePermission, AllowAny
from rest_framework.renderers import BaseRenderer, JSONRenderer
from ..get_throttle_details import get_throttle_details
from ..page_number_pagination import PageNumberPagination
from django.db.models.query import QuerySet

logger = logging.getLogger(__name__)


class ReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only viewset that standardizes API response formatting and error handling."""

    # Response messages
    DEFAULT_ERROR_CODE = "error"
    DEFAULT_ERROR_MESSAGE = "A validation error occurred"
    DEFAULT_SUCCESS_MESSAGE = "Request processed successfully"
    DEFAULT_FAILURE_MESSAGE = "An unexpected error occurred"
    DEFAULT_DELETE_MESSAGE = "Resource deleted successfully"

    # Default configurations
    filter_backends: List[Type[BaseFilterBackend]] = []
    lookup_field: str = 'pk'
    lookup_url_kwarg: Optional[str] = None
    pagination_class: Optional[Type[pagination.PageNumberPagination]] = PageNumberPagination
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    queryset: QuerySet = QuerySet()
    renderer_classes: Optional[List[Type[BaseRenderer]]] = [JSONRenderer]
    search_fields: Optional[Sequence[str]] = ()
    throttle_classes: List[Type[BaseThrottle]] = [AnonRateThrottle]

    def _create_error_dict(self, field: str, error: Any, code: str = DEFAULT_ERROR_CODE) -> Dict[str, Any]:
        """Creates standardized error dictionary with field, code, message and details."""
        if isinstance(error, dict):
            return {
                "field": error.get('field', field),
                "code": error.get('code', code),
                "message": error.get('message', str(error)),
                "details": error.get('details', None)
            }
        return {
            "field": field,
            "code": code,
            "message": str(error),
            "details": None
        }

    def _process_field_errors(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Converts API validation errors to standard format."""
        errors = []
        for field, error_list in data.items():
            if field in ("detail", "message"):
                continue

            field = "none" if field == "non_field_errors" else field

            if isinstance(error_list, list):
                errors.extend([self._create_error_dict(field, error) for error in error_list])
            else:
                errors.append(self._create_error_dict(field, error_list))

        return errors

    def _get_validation_message(self, data: Dict[str, Any]) -> str:
        """Extracts validation message from error data."""
        return data.get("message") or data.get("detail") or self.DEFAULT_ERROR_MESSAGE

    def _build_error_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats error response with message and error details."""
        errors = self._process_field_errors(data)
        error_response = {
            "message": self._get_validation_message(data),
            "errors": errors
        }
        logger.error(f"Error Response: {error_response}")
        return error_response

    def finalize_response(
        self,
        request: Request,
        response: Union[Response, HttpResponseBase],
        *args,
        **kwargs
    ) -> Union[Response, HttpResponseBase]:
        """Finalizes API response format with standard structure and throttling info."""
        data = getattr(response, "data", None)

        if request.method == 'DELETE' and response.status_code == 204:
            custom_response = {
                "message": self.DEFAULT_DELETE_MESSAGE,
                "data": None
            }
            response.status_code = 200
        elif response.status_code >= 400:
            logger.error(f"Request failed with status code {response.status_code}")
            custom_response = (
                self._build_error_response(data) if isinstance(data, dict)
                else {"message": self.DEFAULT_FAILURE_MESSAGE, "errors": []}
            )
        else:
            logger.info(f"Request succeeded with status code {response.status_code}")
            custom_response = {
                "message": self.DEFAULT_SUCCESS_MESSAGE,
                "data": data
            }

        setattr(response, "throttles", get_throttle_details(self))
        setattr(response, "data", custom_response)
        return super().finalize_response(request, response, *args, **kwargs)
