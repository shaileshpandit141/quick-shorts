from apps.user_auth.serializers.user_serializer import UserPublicSerializer
from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from ..models.report import Report

from .short_video_serializer import ShortVideoSerializer


class ReportSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Report"""

    # Call nested serializers
    reported_by = UserPublicSerializer(read_only=True)
    video = ShortVideoSerializer(read_only=True)

    class Meta:
        model = Report
        fields = [
            "id",
            "reported_by",
            "video",
            "reason",
            "status",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "reported_by", "status", "created_at", "updated_at"]
