from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.like import Like
from shorts.serializers.like import LikeSerializer
from rest_core.cache.mixins import CacheMixin


class LikeModelViewSet(CacheMixin, ModelViewSet):
    """Like view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    lookup_field = "id"
    http_method_names = ["get", "post", "delete"]

    def perform_create(self, serializer) -> None:
        """Create a new like video with the owner."""
        serializer.save(user=self.request.user)
