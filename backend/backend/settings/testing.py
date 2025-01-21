# Import all settings from base configuration
from .base import *
from .base import BASE_DIR

# Enable debug mode for development environment
DEBUG = True

# Configure Logging for development
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# Allow all hosts to access the application
ALLOWED_HOSTS = ["*"]

# Enable CORS for all origins
CORS_ALLOW_ALL_ORIGINS = True

# Database configuration using SQLite for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Caches Configuration
# -----------------------
# Memcached configuration for local development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Use MD5 password hashing for testing (not recommended for production)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
