# Import all settings from base configuration
# -------------------------------------------
from .base import *
from .base import BASE_DIR, LOGGING, REST_FRAMEWORK

# Enable debug mode for testing environment
# -----------------------------------------
DEBUG = True

# Configure Logging for testing environment
# -----------------------------------------
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# Allow all hosts for testing environment
# ---------------------------------------
ALLOWED_HOSTS = ["*"]

# Enable CORS for all origins for testing environment
# ---------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# REST Framework Configuration Settings
# -------------------------------------
REST_FRAMEWORK.update(
    {
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
            "rest_framework.renderers.BrowsableAPIRenderer",
        ],
    }
)

# SQLite Database Configuration for testing environment
# -----------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REST_FRAMEWORK.update({"PAGE_SIZE": 2})

# Memcached configuration for testing environment
# -----------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
