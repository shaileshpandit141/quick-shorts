from rest_core.viewsets.mixins import ChoiceFieldViewSetMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet
from short_video.models.comment import Comment
from short_video.serializers.comment_serializer import CommentSerializer


class CommentModelViewSet(
    ChoiceFieldViewSetMixin,
    ModelViewSet,
):
    """Comment view CRUD API view"""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "id"

    def perform_create(self, serializer) -> None:
        """Create a new comment view with the user."""
        serializer.save(user=self.request.user)
