from rest_framework.serializers import ModelSerializer
from ..models.view import View
from rest_core.serializers.mixins import RecordsCreationMixin


class ViewSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for View"""

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
