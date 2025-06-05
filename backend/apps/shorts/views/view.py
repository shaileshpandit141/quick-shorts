from typing import NoReturn

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.view import View
from shorts.serializers.view import ViewSerializer
from rest_core.cache.mixins import CacheMixin


class ViewModelViewSet(CacheMixin, ModelViewSet):
    """Short video view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    lookup_field = "id"
    http_method_names = ["get", "post"]

    def perform_create(self, serializer) -> None:
        """Create a new short video view with the user."""
        serializer.save(user=self.request.user)

    def retrieve(self, request, id) -> NoReturn:
        raise MethodNotAllowed(request.method)
