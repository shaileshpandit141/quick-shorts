from apps.user_auth.serializers.user_serializer import UserPublicSerializer
from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from ..models.like import Like
from .short_video_serializer import ShortVideoSerializer


class LikeSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Like"""

    # Call nested serializers
    user = UserPublicSerializer(read_only=True)
    video = ShortVideoSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ["id", "user", "video", "liked_at", "updated_at"]
        read_only_fields = ["id", "liked_at", "updated_at"]
