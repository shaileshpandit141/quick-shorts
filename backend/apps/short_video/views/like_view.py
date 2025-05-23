from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.like import Like
from short_video.serializers.like_serializer import LikeSerializer


class LikeModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Like view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        """Create a new like video with the owner."""
        serializer.save(user=self.request.user)
