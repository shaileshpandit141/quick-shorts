from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField

from apps.user_auth.serializers.user_serializer import UserPublicSerializer

from ..models.report import Report
from ..models.short_video import ShortVideo
from .short_video_serializer import ShortVideoSerializer


class ReportSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Report"""

    # Call nested serializers
    reported_by = UserPublicSerializer(read_only=True)
    video = ShortVideoSerializer(read_only=True)
    video_id = PrimaryKeyRelatedField(
        queryset=ShortVideo.objects.all(),
        write_only=True,
        source="video",
        required=True,
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "reported_by",
            "video",
            "video_id",
            "reason",
            "status",
            "updated_at",
        ]
        read_only_fields = ["id", "reported_by", "status", "updated_at"]
