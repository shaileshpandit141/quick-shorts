from django.db import models


class Tag(models.Model):
    """Hashtags"""

    class Meta:
        db_table = "tag"
        verbose_name = "tag"
        verbose_name_plural = "tags"
        ordering = ["-updated_at"]

    objects = models.Manager()

    # Model fields for Tag
    name = models.CharField(
        max_length=50,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "max_length": "Ensure this value has at most 50 characters",
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
