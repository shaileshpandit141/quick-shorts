from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.comment import Comment
from short_video.permissions import CanUpdateAndDelete
from short_video.serializers.comment_serializer import CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend

class CommentModelViewSet(ModelViewSet):
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
