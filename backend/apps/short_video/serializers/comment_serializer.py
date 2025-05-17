from rest_framework.serializers import ModelSerializer
from ..models.comment import Comment
from rest_core.serializers.mixins import RecordsCreationMixin


class CommentSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Comment"""

    class Meta:
        model = Comment
        fields = ["id", "user", "video", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
