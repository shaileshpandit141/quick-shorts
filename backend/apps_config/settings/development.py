# Import all Settings from base configuration
# -------------------------------------------
from .base import *
from .base import BASE_DIR
from decouple import config, Csv

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

# SQLite Database Configuration for development environment
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Memcached Configuration for development environment
# ---------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}
