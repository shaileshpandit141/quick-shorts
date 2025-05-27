from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer
from shorts.models.follow import Follow


class FollowSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Follow"""

    class Meta:
        model = Follow
        fields = ["id", "follower", "following"]
        read_only_fields = ["id", "follower"]
