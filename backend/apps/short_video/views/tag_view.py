from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.tag import Tag
from short_video.serializers.tag_serializer import TagSerializer


class TagModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Tag CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = "id"
