from typing import Any, Dict, Optional, List, Type
import logging
from django.db.models import QuerySet
from rest_framework import views
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.throttling import BaseThrottle
from rest_framework.renderers import BaseRenderer
from rest_framework.parsers import BaseParser
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.metadata import BaseMetadata
from rest_framework.versioning import BaseVersioning
from rest_framework.schemas.openapi import AutoSchema
from ..types import ResponseDataType
from ..response import Response
from ..get_throttle_details import get_throttle_details
from ..format_serializer_errors import format_serializer_errors
from ..page_number_pagination import PageNumberPagination


logger = logging.getLogger(__name__)


class APIView(views.APIView):
    """Base API view with helper methods for quick API development"""
    authentication_classes: List[Type[BaseAuthentication]] = []
    permission_classes: List[Type[BasePermission]] = []
    throttle_classes: List[Type[BaseThrottle]] = []
    renderer_classes: List[Type[BaseRenderer]] = []
    parser_classes: List[Type[BaseParser]] = []
    content_negotiation_class: Optional[Type[BaseContentNegotiation]] = None
    metadata_class: Optional[Type[BaseMetadata]] = None
    versioning_class: Optional[Type[BaseVersioning]] = None
    schema: Optional[AutoSchema] = None
    pagination_class: Type[PageNumberPagination] = PageNumberPagination

    def __init__(self, *args, **kwargs) -> None:
        """Initialize view with status attribute"""
        self.status = status
        self.get_throttle_details = get_throttle_details
        self.format_serializer_errors = format_serializer_errors
        super().__init__(*args, **kwargs)

    def get_object(self, model, *args, **kwargs) -> Dict[str, Any] | None:
        """Get single model instance or None if not found"""
        try:
            return model.objects.get(*args, **kwargs)
        except model.DoesNotExist:
            logger.info(f"Object not found for model {model.__name__} with args: {args}, kwargs: {kwargs}")
            return None

    def filter_object(self, model, *args: Any, **kwargs: Any) -> QuerySet:
        """Get filtered queryset for model"""
        logger.debug(f"Filtering {model.__name__} with args: {args}, kwargs: {kwargs}")
        return model.objects.filter(*args, **kwargs)

    def get_query_params(self, param_name: str, default_value=None) -> Any | None:
        """Get query parameter value with optional default"""
        param_value = self.request.query_params.get(param_name, default_value)
        logger.debug(f"Query param {param_name}: {param_value}")
        if param_value is not None:
            return param_value
        return default_value

    def get_paginator(
        self,
        queryset: QuerySet
    ) -> Response:
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
            return paginator.get_paginated_response(page)

        # If no pagination is required
        logger.debug("Returning unpaginated response")
        return self.response({
            "message": "Request was successful",
            "data": queryset  # type: ignore
        }, status=self.status.HTTP_200_OK)

    def response(
        self,
        data: ResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ) -> Response:
        logger.debug(f"Preparing response with status {status}")
        response = Response(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )
        setattr(response, "throttles", get_throttle_details(self))
        return response
