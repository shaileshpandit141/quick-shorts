from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from shorts.models.comment import Comment
from shorts.permissions import CanUpdateAndDelete
from shorts.serializers.comment import CommentSerializer
from rest_core.cache.mixins import CacheMixin


class CommentModelViewSet(CacheMixin, ModelViewSet):
    """Comment view CRUD API view"""

    permission_classes = [IsAuthenticated, CanUpdateAndDelete]
    throttle_classes = [UserRateThrottle]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["video"]

    def perform_create(self, serializer) -> None:
        """Create a new comment view with the user."""
        serializer.save(owner=self.request.user)
