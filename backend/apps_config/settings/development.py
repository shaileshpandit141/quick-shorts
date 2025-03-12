# Import all Settings from base configuration
# -------------------------------------------
from decouple import Csv, config

from .base import *
from .base import BASE_DIR, LOGGING, REST_FRAMEWORK

# Enable debug mode for development purposes only
# -----------------------------------------------
DEBUG = True

# Configure Logging for development
# ---------------------------------
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# List of host/domain names that Django can serve
# -----------------------------------------------
ALLOWED_HOSTS = config("HOST", cast=Csv())

# Configure CORS Settings
# -----------------------
CORS_ALLOWED_ORIGINS = config("FRONTEND_URL", cast=Csv())

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

REST_FRAMEWORK.update({"PAGE_SIZE": 4})
REST_FRAMEWORK.update({"MAX_PAGE_SIZE": 8})

# SQLite Database Configuration for development environment
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Memcached configuration for testing environment
# -----------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
