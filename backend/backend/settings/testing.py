# Import all settings from base configuration
from .base import *

# Enable debug mode for development environment
DEBUG = True

# Allow all hosts to access the application
ALLOWED_HOSTS = ["*"]

# Enable CORS for all origins
CORS_ALLOW_ALL_ORIGINS = True 

# Database configuration using SQLite for testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3", # SQLite engine
        "NAME": BASE_DIR / "db.sqlite3",  # Database file path
    }
}

# Use MD5 password hashing for testing (not recommended for production)  
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
