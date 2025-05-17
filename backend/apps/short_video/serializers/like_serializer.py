from rest_framework.serializers import ModelSerializer
from ..models.like import Like
from rest_core.serializers.mixins import RecordsCreationMixin


class LikeSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Like"""

    class Meta:
        model = Like
        fields = ["id", "user", "video", "liked_at", "updated_at"]
        read_only_fields = ["id", "liked_at", "updated_at"]
