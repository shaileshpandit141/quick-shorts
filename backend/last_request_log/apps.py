from django.apps import AppConfig


class LastRequestLogConfig(AppConfig):
    """Django app configuration for request logging."""

    default_auto_field = "django.db.models.BigAutoField"  # type: ignore
    name = "last_request_log"
