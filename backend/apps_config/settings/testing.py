# Import all settings from base configuration
# -------------------------------------------
from .base import *
from .base import BASE_DIR, LOGGING

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

# Allowed All CSP_FRAME_ANCESTORS by Configuration Content-Security-Policy Settings
# -----------------------------------------------------------------------------
CSP_FRAME_ANCESTORS = ["*"]

# SQLite Database Configuration for testing environment
# -----------------------------------------------------
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
