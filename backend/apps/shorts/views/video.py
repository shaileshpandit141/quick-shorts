from django_filters.rest_framework import DjangoFilterBackend
from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.video import Video
from shorts.permissions import CanUpdateAndDelete
from shorts.serializers.video import VideoSerializer
from shorts.filters import VideoFilterSet


class VideoModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Short video CRUD API view"""

    permission_classes = [IsAuthenticated, CanUpdateAndDelete]
    throttle_classes = [UserRateThrottle]
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = "id"
    choice_fields = ["privacy"]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = VideoFilterSet
    # filterset_fields = ["owner", "tags"]
    search_fields = ["caption"]
    ordering_fields = ["id", "updated_at"]

    def perform_create(self, serializer) -> None:
        """Create a new short video with the owner."""
        serializer.save(owner=self.request.user)
