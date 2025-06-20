from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Follow(models.Model):
    """Follow system"""

    class Meta:
        db_table = "follow"
        verbose_name = "follow"
        verbose_name_plural = "follows"
        ordering = ["-followed_at"]
        unique_together = ("follower", "following")

    objects = models.Manager()

    # Model fields for Follow
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follows_as_follower",
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "does_not_exist": "Object does not exist",
        },
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follows_as_following",
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "does_not_exist": "Object does not exist",
        },
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.follower.email} follows {self.following.email}"
