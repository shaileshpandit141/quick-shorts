from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Django app configuration for the users app."""

    default_auto_field = "django.db.models.BigAutoField" # type: ignore
    name = "users"
