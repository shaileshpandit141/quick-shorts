from rest_framework.serializers import ModelSerializer
from ..models.report import Report
from rest_core.serializers.mixins import RecordsCreationMixin


class ReportSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Report"""

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
