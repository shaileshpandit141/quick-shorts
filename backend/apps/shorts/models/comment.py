from django.contrib.auth import get_user_model
from django.db import models

from .video import Video

User = get_user_model()


class Comment(models.Model):
    """Comments on videos"""

    class Meta:
        db_table = "comment"
        verbose_name = "comment"
        verbose_name_plural = "comments"
        ordering = ["-updated_at"]

    objects = models.Manager()

    # Model fields for Comment
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name="comments_as_owner",
        related_query_name=None,
        limit_choices_to={},
        parent_link=False,
        blank=False,
        null=False,
        db_index=True,
        db_constraint=True,
        error_messages={
            "invalid": "Invalid value",
            "invalid_choice": "Select a valid choice",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "does_not_exist": "Object does not exist",
        },
    )
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name="comments_as_video",
        related_query_name=None,
        limit_choices_to={},
        parent_link=False,
        blank=False,
        null=False,
        db_index=True,
        db_constraint=True,
        error_messages={
            "invalid": "Invalid value",
            "invalid_choice": "Select a valid choice",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "does_not_exist": "Object does not exist",
        },
    )
    content = models.TextField(
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        },
    )
    comment_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.owner.email} Comment {self.video.caption}"
