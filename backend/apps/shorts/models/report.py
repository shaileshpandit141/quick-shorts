from django.contrib.auth import get_user_model
from django.db import models

from .video import Video

User = get_user_model()


class Report(models.Model):
    """Report inappropriate videos"""

    class Meta:
        db_table = "report"
        verbose_name = "report"
        verbose_name_plural = "reports"
        ordering = ["-updated_at"]
        unique_together = ("reported_by", "video")

    objects = models.Manager()

    # Report status choices
    REPORT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("resolved", "Resolved"),
        ("rejected", "Rejected"),
    ]

    # Model fields for Report
    reported_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reports_made",
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
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        related_name="reports_received",
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
    reason = models.TextField(
        blank=False,
        null=False,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        },
    )
    status = models.CharField(
        max_length=20,
        choices=REPORT_STATUS_CHOICES,
        default="pending",
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        },
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Report by {self.reported_by.email} on video {self.video.pk}"
