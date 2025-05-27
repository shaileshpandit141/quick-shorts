from django.contrib.auth import get_user_model
from django.db import models

from .tag import Tag

User = get_user_model()


class ShortVideo(models.Model):
    """ShortVideo model class"""

    class Meta:
        db_table = "short_video"
        verbose_name = "short video"
        verbose_name_plural = "short videos"
        ordering = ["-updated_at"]

    objects = models.Manager()

    PRIVACY_CHOICES = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    # Model fields for ShortVideo
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
        related_name="shorts",
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
    title = models.CharField(
        max_length=120,
        unique=True,
        blank=False,
        null=False,
        db_index=True,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "max_length": "Ensure this value has at most 120 characters",
        },
    )
    description = models.TextField(
        blank=True,
        null=True,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Enter a valid value",
        },
    )
    video = models.FileField(
        upload_to="shorts/videos/",
        max_length=100,
        blank=False,
        null=False,
        storage=None,
        db_index=False,
        error_messages={
            "invalid": "No file was submitted",
            "missing": "No file was submitted",
            "empty": "The submitted file is empty",
            "max_length": "Ensure this filename has at most 100 characters",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        },
    )
    thumbnail = models.ImageField(
        upload_to="shorts/thumbnails/",
        max_length=100,
        blank=True,
        null=True,
        storage=None,
        db_index=False,
        default=None,
        error_messages={
            "invalid": "Invalid image file",
            "invalid_image": "Upload a valid image.",
            "missing": "No file was submitted",
            "empty": "The submitted file is empty",
            "max_length": "Ensure this filename has at most 100 characters",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        },
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="short_videos",
        related_query_name=None,
        db_constraint=True,
        blank=False,
        error_messages={
            "invalid": "Invalid value",
            "invalid_choice": "Select a valid tags.",
            "invalid_pk_value": "Invalid primary key value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        },
    )
    privacy = models.CharField(
        max_length=10,
        unique=False,
        blank=True,
        null=True,
        db_index=True,
        choices=PRIVACY_CHOICES,
        default="public",
        error_messages={
            "invalid": "Please choose a valid privacy",
            "max_length": "Ensure this value has at most 10 characters",
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
