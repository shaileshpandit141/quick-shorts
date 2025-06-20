from typing import NoReturn

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.tag import Tag
from shorts.serializers.tag import TagSerializer
from rest_core.cache.mixins import CacheMixin


class TagModelViewSet(CacheMixin, ModelViewSet):
    """Tag CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "id"
    http_method_names = ["get", "post"]

    def retrieve(self, request, id) -> NoReturn:
        raise MethodNotAllowed(request.method)
