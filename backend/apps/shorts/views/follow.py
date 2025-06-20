from django.db.models.manager import BaseManager
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.follow import Follow
from shorts.serializers.follow import FollowSerializer
from rest_core.cache.mixins import CacheMixin


class FollowModelViewSet(CacheMixin, ModelViewSet):
    """Follow view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "delete"]

    def perform_create(self, serializer) -> None:
        """Create a new follow view with the user."""
        serializer.save(follower=self.request.user)

    def get_queryset(self) -> BaseManager[Follow]:  # type: ignore
        """Get the queryset for the follow view."""
        return Follow.objects.filter(follower=self.request.user)
