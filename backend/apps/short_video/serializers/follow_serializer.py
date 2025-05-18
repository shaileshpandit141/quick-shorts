from rest_core.serializers.mixins import RecordsCreationMixin
from rest_framework.serializers import ModelSerializer

from apps.user_auth.serializers.user_serializer import UserPublicSerializer

from ..models.follow import Follow


class FollowSerializer(RecordsCreationMixin, ModelSerializer):
    """Serializer class for Follow"""

    # Call nested serializers
    follower = UserPublicSerializer(read_only=True)
    following = UserPublicSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ["id", "follower", "following", "followed_at", "updated_at"]
        read_only_fields = ["id", "followed_at", "updated_at"]
