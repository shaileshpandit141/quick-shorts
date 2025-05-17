from rest_framework.serializers import ModelSerializer
from ..models.follow import Follow
from rest_core.serializers.mixins import RecordsCreationMixin


class FollowSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Follow"""

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "followed_at", "updated_at"]
        read_only_fields = ["id", "followed_at", "updated_at"]
