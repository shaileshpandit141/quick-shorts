import logging
from typing import Any, Dict, List, Optional, Type

from django.db.models import QuerySet
from rest_framework import status, views
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.throttling import BaseThrottle

from ..format_serializer_errors import format_serializer_errors
from ..get_throttle_details import get_throttle_details
from ..page_number_pagination import PageNumberPagination
from ..response import Response
from ..types import ResponseDataType

logger = logging.getLogger(__name__)


class APIView(views.APIView):
    """Base API view with helper methods for quick API development"""

    permission_classes: List[Type[BasePermission]] = [AllowAny]
    throttle_classes: List[Type[BaseThrottle]] = []
    renderer_classes: List[Type[BaseRenderer]] = [JSONRenderer]
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
            logger.info(
                f"Object not found for model {model.__name__} with args: {args}, kwargs: {kwargs}"
            )
            return None

    def filter_object(self, model, *args: Any, **kwargs: Any) -> QuerySet:
        """Get filtered queryset for model"""
        logger.debug(f"Filtering {model.__name__} with args: {args}, kwargs: {kwargs}")
        return model.objects.filter(*args, **kwargs)

    def get_query_params(self, param_name: str, default_value=None) -> Any | None:
        """Get query parameter value with optional default"""
        param_value = self.request.GET.get(param_name, default_value)
        logger.debug(f"Query param {param_name}: {param_value}")
        if param_value is not None:
            return param_value
        return default_value

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

    def response(
        self,
        data: ResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None,
    ) -> Response:
        logger.debug(f"Preparing response with status {status}")
        response = Response(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type,
        )
        setattr(response, "throttles", get_throttle_details(self))
        return response
