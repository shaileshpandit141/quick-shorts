from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer, ValidationError
from shorts.models.report import Report


class ReportSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Report"""

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

    def validate(self, attrs: dict[str, str]) -> dict[str, str]:
        """Validating unique reports on a video"""

        # Get required fields.
        user = self.context["request"].user
        video = attrs.get("video")

        # Check if already reported this video or not.
        if Report.objects.filter(reported_by=user, video=video).exists():
            raise ValidationError("You have already reported this video.")

        # Return validated data
        return attrs
