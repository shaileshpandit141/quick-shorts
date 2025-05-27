from rest_core.serializers.mixins import FileFieldUrlMixin, RecordsCreationMixin
from rest_framework.serializers import ModelSerializer
from shorts.models.video import Video
from user_auth.serializers.user_serializers import UserPublicSerializer

from .tag import TagSerializer


class VideoSerializer(RecordsCreationMixin, FileFieldUrlMixin, ModelSerializer):
    """Serializer class for Video"""

    # Call nested serializers
    owner = UserPublicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "owner",
            "video",
            "thumbnail",
            "caption",
            "tags",
            "privacy",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "updated_at"]
