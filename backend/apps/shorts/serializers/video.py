from rest_core.serializers.mixins import FileFieldUrlMixin, RecordsCreationMixin
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from shorts.models.comment import Comment
from shorts.models.like import Like
from shorts.models.video import Video
from shorts.models.view import View
from user_auth.serializers.user_serializers import UserPublicSerializer

from .tag import TagSerializer


class VideoSerializer(RecordsCreationMixin, FileFieldUrlMixin, ModelSerializer):
    """Serializer class for Video"""

    # Call nested serializers
    owner = UserPublicSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    total_views = SerializerMethodField()
    total_likes = SerializerMethodField()
    total_comments = SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            "id",
            "owner",
            "video",
            "thumbnail",
            "caption",
            "tags",
            "total_views",
            "total_likes",
            "total_comments",
            "privacy",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "updated_at",
        ]

    def get_total_views(self, obj) -> int:
        return View.objects.filter(video=obj.id).count()

    def get_total_likes(self, obj) -> int:
        return Like.objects.filter(video=obj.id).count()

    def get_total_comments(self, obj) -> int:
        return Comment.objects.filter(video=obj.id).count()
