from django.contrib.auth import get_user_model
from django.db import models

from .video import Video

User = get_user_model()


class Like(models.Model):
    """User likes a video"""

    class Meta:
        db_table = "like"
        verbose_name = "like"
        verbose_name_plural = "likes"
        ordering = ["-liked_at"]
        unique_together = ("video", "user")

    objects = models.Manager()

    # Model fields for Like
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name="likes_as_user",
        related_query_name=None,
        limit_choices_to={},
        parent_link=False,
        blank=False,
        null=False,
        db_index=True,
        db_constraint=True,
        error_messages={
            "invalid": "Invalid value",
            "invalid_choice": "Select a valid user.",
            "does_not_exist": "Object does not exist",
        },
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name="likes_as_video",
        related_query_name=None,
        limit_choices_to={},
        parent_link=False,
        blank=False,
        null=False,
        db_index=True,
        db_constraint=True,
        error_messages={
            "invalid": "Invalid value",
            "invalid_choice": "Select a valid choice.",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "does_not_exist": "Object does not exist",
        },
    )
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.email} liked {self.video.title}"
