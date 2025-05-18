from rest_core.serializers.mixins import FileFieldUrlMixin, RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from apps.user_auth.serializers.user_serializer import UserPublicSerializer

from ..models.short_video import ShortVideo
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
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]
