from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from apps.user_auth.serializers.user_serializer import UserPublicSerializer

from ..models.comment import Comment


class CommentSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Comment"""

    # Call nested serializers
    user = UserPublicSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "video", "content", "updated_at"]
        read_only_fields = ["id", "user", "updated_at"]
