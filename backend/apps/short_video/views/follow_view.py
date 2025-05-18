from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.follow import Follow
from short_video.serializers.follow_serializer import FollowSerializer


class FollowViewModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Follow view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        """Create a new follow view with the user."""
        serializer.save(follower=self.request.user)
