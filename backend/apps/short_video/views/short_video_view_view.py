from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.view import View
from short_video.serializers.view_serializer import ViewSerializer


class ShortVideoViewModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """ShortVideoView CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    lookup_field = "pk"

    def perform_create(self, serializer) -> None:
        """Create a new short video with the owner."""
        serializer.save(user=self.request.user)
