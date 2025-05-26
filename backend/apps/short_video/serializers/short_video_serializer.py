from rest_core.serializers.mixins import FileFieldUrlMixin, RecordsCreationMixin
from rest_framework.serializers import ModelSerializer
from short_video.models.short_video import ShortVideo
from user_auth.serializers.user_serializers import UserPublicSerializer

from .tag_serializer import TagSerializer


class ShortVideoSerializer(RecordsCreationMixin, FileFieldUrlMixin, ModelSerializer):
    """Serializer class for ShortVideo"""

    # Call nested serializers
    owner = UserPublicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = ShortVideo
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "video",
            "thumbnail",
            "tags",
            "privacy",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "updated_at"]
