from typing import Any, Dict, Optional
from django.db.models import QuerySet
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from .types import ThrottleType, DataType
from .get_meta import get_meta


class QuickAPIView(APIView):
    """Base API view with helper methods for quick API development"""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize view with status attribute"""
        self.status = status
        super().__init__(*args, **kwargs)

    def get_throttle_class(self) -> ThrottleType | None:
        """Get the first throttle class if defined, otherwise None"""
        throttle_classes = getattr(self, 'throttle_classes', None)
        if throttle_classes and len(throttle_classes) > 0:
            return throttle_classes[0]
        return None

    def response(
        self,
        data: DataType,
        status=None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ) -> Response:
        """
        Create standardized API response with status, message, data, errors and meta info.
        Optionally includes pagination data if provided.
        """
        payload: DataType = {
            "status": data["status"],
            "message": data["message"],
            "data": data.get("data", None),
            "errors": data.get("errors", None),
            "meta": get_meta(
                self.request,
                self.get_throttle_class()
            )
        }

        pagination = data.get("pagination", None)
        if pagination is not None:
            payload["pagination"] = pagination

        return Response(
            data=payload,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )

    def get_query(self, model, *args, **kwargs) -> Dict[str, Any] | None:
        """Get single model instance or None if not found"""
        try:
            return model.objects.get(*args, **kwargs)
        except model.DoesNotExist:
            return None

    def get_query_params(self, param_name: str, default_value=None) -> Any | None:
        """Get query parameter value with optional default"""
        param_value = self.request.query_params.get(param_name, default_value)
        if param_value is not None:
            return param_value
        return default_value

    def get_queryset(self, model, *args: Any, **kwargs: Any) -> QuerySet:
        """Get filtered queryset for model"""
        return model.objects.filter(*args, **kwargs)

    def get_paginator(
        self,
        queryset: QuerySet,
        page_number: Optional[int] = None,
        items_per_page: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Returns pagination data for the given queryset.
        Uses page and items-per-page query params if not explicitly provided.
        Default page is 1, default items per page is 10.
        """
        param_page = self.get_query_params("page", "1")
        param_items = self.get_query_params("items-per-page", "10")

        page_number = page_number or int(param_page) if param_page is not None else 1
        items_per_page = items_per_page or int(param_items) if param_items is not None else 10

        paginator = Paginator(queryset, items_per_page)
        page = paginator.get_page(page_number)

        paginated_data = {
            "current_page": page.number,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
            "items_per_page": items_per_page,
            "has_next": page.has_next(),
            "has_previous": page.has_previous()
        }
        return paginated_data

    def handle_exception(self, exc: Exception) -> Response:
        """Handle API exceptions, providing standardized error responses"""
        if isinstance(exc, MethodNotAllowed):
            return self.response({
                "status": "failed",
                "message": "Method not allowed",
                "data": None,
                "errors": [
                    {
                        "field": "none",
                        "code": "method_not_allowed", 
                        "message": "The requested HTTP method is not allowed for this endpoint",
                        "details": None
                    }
                ]
            }, self.status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().handle_exception(exc)
