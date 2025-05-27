from django_filters.rest_framework import DjangoFilterBackend
from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.short_video import ShortVideo
from short_video.permissions import CanUpdateAndDelete
from short_video.serializers.short_video_serializer import ShortVideoSerializer
from short_video.filters import ShortVideoFilterSet

class ShortVideoModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Short video CRUD API view"""

    permission_classes = [IsAuthenticated, CanUpdateAndDelete]
    throttle_classes = [UserRateThrottle]
    queryset = ShortVideo.objects.all()
    serializer_class = ShortVideoSerializer
    lookup_field = "id"
    choice_fields = ["privacy"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ShortVideoFilterSet
    # filterset_fields = ["owner", "tags"]
    search_fields = ["title", "description"]
    ordering_fields = ["id", "updated_at"]

    def perform_create(self, serializer) -> None:
        """Create a new short video with the owner."""
        serializer.save(owner=self.request.user)
