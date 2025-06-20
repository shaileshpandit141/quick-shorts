from django.contrib.auth import get_user_model
from django.db import models

from .video import Video

User = get_user_model()


class View(models.Model):
    """Model class for View"""

    class Meta:
        db_table = "view"
        verbose_name = "view"
        verbose_name_plural = "views"
        ordering = ["-timestamp"]

    objects = models.Manager()

    # Model fields for View
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        primary_key=False,
        related_name="views_as_user",
        related_query_name=None,
        limit_choices_to={},
        parent_link=False,
        blank=True,
        null=True,
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
        related_name="views_as_video",
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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        user = getattr(self.user, "username", "Unknown")
        return f"{user} viewed {self.video.caption}"
