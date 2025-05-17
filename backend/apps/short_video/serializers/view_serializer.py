from apps.user_auth.serializers.user_serializer import UserPublicSerializer
from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from ..models.view import View
from .short_video_serializer import ShortVideoSerializer


class ViewSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for View"""

    # Call nested serializers
    user = UserPublicSerializer(read_only=True)
    video = ShortVideoSerializer(read_only=True)

    class Meta:
        model = View
        fields = [
            "id",
            "user",
            "video",
            "timestamp",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "timestamp", "updated_at"]
