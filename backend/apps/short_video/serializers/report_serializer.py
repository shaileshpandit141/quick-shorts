from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from short_video.models.report import Report
from short_video.models.short_video import ShortVideo
from user_auth.serializers.user_serializer import UserSerializer

from .short_video_serializer import ShortVideoSerializer


class ReportSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Report"""

    # Call nested serializers
    reported_by = UserSerializer(read_only=True)
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
