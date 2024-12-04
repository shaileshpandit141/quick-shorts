from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Django app configuration for the users app.

    This class configures the users app's settings including the default
    auto field type and app name.

    Attributes:
        default_auto_field (str): The default auto field type to use for models
        in this app. Set to Django's BigAutoField.
        name (str): The name of this Django app, set to 'users'.
    """
    default_auto_field = 'django.db.models.BigAutoField' # type: ignore
    name = 'users'
