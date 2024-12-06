# Import all settings from base configuration
from .base import *

# Enable debug mode for development purposes only
DEBUG = True

# List of host/domain names that Django can serve
ALLOWED_HOSTS = [config("HOST", cast=str)]

# Cross-Origin Resource Sharing (CORS) Settings
# -----------------------
# Allows requests from any origin - only for development
CORS_ALLOW_ALL_ORIGINS = True

# Database Configuration
# -----------------------
# SQLite configuration for local development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Password hashing algorithms in order of preference
# -----------------------
# Using multiple algorithms provides additional security layers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',    # Recommended primary hasher
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',    # Strong fallback option
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher', # Additional fallback
    'django.contrib.auth.hashers.ScryptPasswordHasher',    # Final fallback option
]
