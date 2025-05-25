from typing import NoReturn

from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.tag import Tag
from short_video.serializers.tag_serializer import TagSerializer


class TagModelViewSet(ModelViewSet):
    """Tag CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "id"
    http_method_names = ["get", "post"]

    def retrieve(self, request, id) -> NoReturn:
        raise MethodNotAllowed(request.method)
