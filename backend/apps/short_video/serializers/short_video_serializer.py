from rest_framework.serializers import ModelSerializer
from ..models.short_video import ShortVideo
from rest_core.serializers.mixins import RecordsCreationMixin


class ShortVideoSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for ShortVideo"""

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
