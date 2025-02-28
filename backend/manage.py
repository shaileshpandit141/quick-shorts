"""
Django's command-line utility for administrative tasks.
This script serves as the main entry point for Django management commands.
It handles configuration of the Django environment and executes administrative tasks.
"""

import os
import sys

from decouple import config


def main() -> None:
    """
    Main function that runs Django administrative tasks.

    This function:
    1. Sets up the Django settings module
    2. Configures host and port from environment variables
    3. Executes Django management commands

    The host and port can be configured via environment variables:
    - HOST: The host to run the server on (default: localhost)
    - PORT: The port number to use (default: 8000)
    """
    # Set the Django settings module path
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "apps_config.settings")

    # Load host and port configuration from environment variables
    # using python-decouple for safer configuration management
    HOST = config("HOST", cast=str, default="localhost")
    PORT = config("PORT", cast=int, default=8000)

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # If no command is provided or the command is 'runserver',
    # append the host:port configuration to the command
    if len(sys.argv) == 1 or sys.argv[1] == "runserver":
        sys.argv = sys.argv[:2] + [f"{HOST}:{PORT}"]

    # Execute the Django management command
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
