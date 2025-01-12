from typing import Any, Dict, Optional
from django.db.models import QuerySet
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework import status
from ..types import (
    ResponseDataType,
    SuccessResponseDataType,
    ErrorResponseDataType,
    MetaType
)
from ..response import Response
from ..get_throttle_details import get_throttle_details


class QuickAPIView(APIView):
    """Base API view with helper methods for quick API development"""

    def __init__(self, *args, **kwargs) -> None:
        """Initialize view with status attribute"""
        self.status = status
        self.get_throttle_details = get_throttle_details
        super().__init__(*args, **kwargs)

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

    def __get_meta(self, meta: MetaType | None) -> MetaType:
        if meta is None:
            return {
                "rate_limit": get_throttle_details(self)
            }
        else:
            return {
                **meta,
                "rate_limit": get_throttle_details(self)
            }

    def response(
        self,
        data: ResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ) -> Response:
        meta = data.get("meta", None)
        data.update({
            "meta": self.__get_meta(meta)}
        )
        return Response(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )

    def success_response(
        self,
        data: SuccessResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ) -> Response:
        meta = data.get("meta", None)
        payload: ResponseDataType = {
            "status": "succeeded",
            "message": data["message"],
            "data": data["data"],
            "errors": None,
            "meta": self.__get_meta(meta)
        }

        return Response(
            data=payload,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )

    def error_response(
        self,
        data: ErrorResponseDataType,
        status: Optional[int] = None,
        template_name: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        exception: bool = False,
        content_type: Optional[str] = None
    ) -> Response:
        meta = data.get("meta", None)
        payload: ResponseDataType = {
            "status": "failed",
            "message": data["message"],
            "data": None,
            "errors": data["errors"],
            "meta": self.__get_meta(meta)
        }

        return Response(
            data=payload,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )
