from django.db import models


class LastRequestLog(models.Model):
    """Model to log HTTP request details and responses."""

    objects = models.Manager()

    class Meta:
        db_table = "last request log"
        verbose_name = "last request log"
        verbose_name_plural = "last request logs"
        ordering = ["-id"]
        unique_together = ()

    user = models.CharField(
        max_length=255,
        unique=False,
        null=True,
        blank=False,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "max_length": "Ensure this value has at most 255 characters"
        }
    )
    path = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "max_length": "Ensure this value has at most 255 characters"
        }
    )
    method = models.CharField(
        max_length=10,
        unique=False,
        null=False,
        blank=False,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "max_length": "Ensure this value has at most 10 characters"
        }
    )
    ip = models.GenericIPAddressField(
        protocol="both",
        unpack_ipv4=False,
        null=True,
        blank=True,
        db_index=False,
        default=None,
        error_messages={
            "invalid": "Enter a valid IPv4 or IPv6 address",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank"
        }
    )
    timestamp = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        null=True,
        blank=True,
        db_index=False,
        error_messages={
            "invalid": "Enter a valid date/time",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank"
        }
    )
    response_time = models.CharField(
        max_length=25,
        unique=False,
        null=False,
        blank=False,
        db_index=False,
        default="",
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
            "max_length": "Ensure this value has at most 16 characters"
        }
    )
    is_authenticated = models.BooleanField(
        default=models.NOT_PROVIDED,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        }
    )
    is_api_request = models.BooleanField(
        default=models.NOT_PROVIDED,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        }
    )
    is_request_success = models.BooleanField(
        default=models.NOT_PROVIDED,
        null=False,
        db_index=False,
        error_messages={
            "invalid": "Invalid value",
            "null": "This field cannot be null",
            "blank": "This field cannot be blank",
        }
    )

    def add_default_value(self, field: str, value: bool) -> None:
        """Sets the provided default value for a field if it is None."""
        if getattr(self, field) is None:
            setattr(self, field, value)

    def save(self, *args, **kwargs):
        """Saves the request log after setting default values for boolean fields."""
        default_values = {
            "is_authenticated": False,
            "is_request_success": False,
            "is_api_request": False
        }
        for field, value in default_values.items():
            self.add_default_value(field, value)

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user} | {self.ip} | {self.method} | {self.is_request_success}"
