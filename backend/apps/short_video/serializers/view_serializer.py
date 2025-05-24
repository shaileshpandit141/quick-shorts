from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer
from short_video.models.view import View

class ViewSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for View"""

    class Meta:
        model = View
        fields = ["id", "user", "video", "timestamp"]
        read_only_fields = ["id", "user", "timestamp"]
