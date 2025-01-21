# Import all settings from base configuration
from .base import *
from .base import BASE_DIR
from decouple import config, Csv

# Enable debug mode for development purposes only
DEBUG = True

# Configure Logging for development
LOGGING["loggers"]["django"]["level"] = "DEBUG"

# List of host/domain names that Django can serve
ALLOWED_HOSTS = config("HOST", cast=Csv())
CORS_ALLOWED_ORIGINS = config("FRONTEND_URL", cast=Csv())

# Database Configuration
# -----------------------
# SQLite configuration for local development
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
        "BACKEND": "django.core.cache.backends.memcached.PyMemcacheCache",
        "LOCATION": "127.0.0.1:11211",
    }
}

# Password hashing algorithms in order of preference
# -----------------------
# Using multiple algorithms provides additional security layers
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",    # Recommended primary hasher
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",    # Strong fallback option
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher", # Additional fallback
    "django.contrib.auth.hashers.ScryptPasswordHasher",    # Final fallback option
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher"
]
