import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Type, TypeVar
from uuid import uuid4

from django.db.models import Model, QuerySet
from django.http.response import HttpResponseBase
from rest_framework.exceptions import APIException, NotFound
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.throttling import AnonRateThrottle, BaseThrottle
from rest_framework.views import APIView

from ..page_number_pagination import PageNumberPagination
from ..throttle_inspector import ThrottleInspector
from .base_api_response_handler import BaseAPIResponseHandler

logger = logging.getLogger(__name__)

# Define a TypeVar that must be a subclass of Model
TypeModel = TypeVar("TypeModel", bound=Model)


class BaseAPIView(BaseAPIResponseHandler, APIView):
    permission_classes: List[Type[BasePermission]] = [AllowAny]
    throttle_classes: List[Type[BaseThrottle]] = [AnonRateThrottle]
    pagination_class: Type[PageNumberPagination] = PageNumberPagination
    serializer_class: Optional[Type[ModelSerializer]] = None
    queryset: Optional[QuerySet] = None

    def get_serializer(self, *args, **kwargs) -> ModelSerializer:
        """Return the class to use for the serializer."""
        serializer = self.get_serializer_class()
        if serializer is None:
            logger.error("Serializer class is None. Cannot serialize page data.")
            raise APIException(detail="Something went wrong!", code=500)
        else:
            # This automatically includes the request boject in the serializer context.
            kwargs.setdefault("context", {}).update({"request": self.request})
            return serializer(*args, **kwargs)

    def get_serializer_class(self) -> Type[ModelSerializer] | None:
        """Return the class to use for the serializer. Defaults
        to using `self.get_serializer_class`.
        """
        return self.serializer_class

    def finalize_response(
        self, request, response, *args, **kwargs
    ) -> Response | HttpResponseBase:
        # Initialize ThrottleInspector class
        throttle_inspector = ThrottleInspector(self)

        # Inspect the throttles details
        throttle_details = throttle_inspector.get_details()

        # Attach throttle details in headers
        throttle_inspector.attach_headers(response, throttle_details)

        # Generate the uuid4 token
        request_id = str(uuid4())

        # Base response structure
        payload = {
            "status": "succeeded" if response.status_code < 400 else "failed",
            "status_code": response.status_code,
            **response.data,
            "meta": {
                "response_time": "N/A",
                "request_id": request_id,
                "timestamp": datetime.utcnow().isoformat(),
                "documentation_url": "https://github.com/shaileshpandit141/django-react-typescript-initial-code/tree/main",
                "rate_limits": throttle_details,
            },
        }

        # Update the response data to use updated data
        setattr(response, "data", payload)

        # Attach meta details in headers
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

        # Call to super methods to handle rest process.
        return super().finalize_response(request, response, *args, **kwargs)

    def get_object(self, model: Type[TypeModel], *args, **kwargs) -> TypeModel | None:
        """Get single model instance or None if not found"""
        try:
            obj = model.objects.get(*args, **kwargs)
            self.check_object_permissions(self.request, obj)
            return obj
        except model.DoesNotExist:
            logger.info(
                f"Object not found for model {model.__name__} with args: {args}, kwargs: {kwargs}"
            )
            return None

    def get_paginated_data(
        self, filter_kwargs: dict[str, Any] | None = None
    ) -> Dict[str, Any]:
        """
        Returns pagination data for the given queryset.
        Uses page and items-per-page query params if not explicitly provided.
        Default page is 1, default items per page is 10.
        """
        logger.debug("Starting pagination process using pagination_class.")
        paginator = self.pagination_class()

        # Check if user want to filter queryset
        if filter_kwargs is not None:
            if self.queryset is not None:
                self.queryset = self.queryset.filter(**filter_kwargs)

        # Paginate the queryset
        page = paginator.paginate_queryset(self.queryset, self.request)
        logger.debug(f"Paginated queryset: {page}")

        if page is None:
            logger.warning("Paginated page is None. Object not found.")
            raise NotFound(detail="The requested object was not found.")

        serializer = self.get_serializer(instance=page, many=True)
        logger.debug("Serializer data prepared for the paginated page.")

        result = {
            "current_page": paginator.page.number,
            "total_pages": paginator.page.paginator.num_pages,
            "total_items": paginator.page.paginator.count,
            "items_per_page": paginator.page.paginator.per_page,
            "has_next": paginator.page.has_next(),
            "has_previous": paginator.page.has_previous(),
            "next_page_number": (
                paginator.page.next_page_number() if paginator.page.has_next() else None
            ),
            "previous_page_number": (
                paginator.page.previous_page_number()
                if paginator.page.has_previous()
                else None
            ),
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "results": getattr(serializer, "data", {}),
        }

        logger.debug(f"Pagination data calculated: {result}")
        return result
