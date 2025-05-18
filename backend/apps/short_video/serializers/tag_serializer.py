from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from ..models.tag import Tag


class TagSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Tag"""

    class Meta:
        model = Tag
        fields = ["id", "name"]
        read_only_fields = ["id"]
