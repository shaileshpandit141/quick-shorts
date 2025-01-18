# Import all settings from base configuration
from .base import *
from decouple import config, Csv

# Disable debug mode for production environment for security
# DEBUG = False
DEBUG = True

# Configure Logging for production
LOGGING['loggers']['django']['level'] = 'INFO'

# Configure allowed hosts and CORS origins from environment variables
# -----------------------
# These should be comma-separated lists in the environment configuration
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
CORS_ALLOWED_ORIGINS = config("CORS_ALLOWED_ORIGINS", cast=Csv())

# PostgreSQL database configuration
# All sensitive credentials are loaded from environment variables
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", cast=str),
        "USER": config("DB_USER", cast=str),
        "PASSWORD": config("DB_PASSWORD", cast=str),
        "HOST": config("DB_HOST", cast=str),
        "PORT": config("DB_PORT", cast=str),
    }
}

# Caches Configuration
# -----------------------
# Redis configuration for local production
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config("REDIS_CACHE_LOCATION", cast=str),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


# Security settings for production environment
# -----------------------
# These settings ensure secure communication and protect against common vulnerabilities
CSRF_COOKIE_SECURE = True  # Enforce HTTPS for CSRF cookies
SESSION_COOKIE_SECURE = True  # Enforce HTTPS for session cookies
SECURE_BROWSER_XSS_FILTER = True  # Activate browser's XSS filtering
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-type sniffing security risks
SECURE_SSL_REDIRECT = True  # Force all connections to use HTTPS

# Password hashing algorithms in order of preference
# -----------------------
# Using multiple algorithms provides additional security layers
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',    # Recommended primary hasher
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',    # Strong fallback option
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher', # Additional fallback
    'django.contrib.auth.hashers.ScryptPasswordHasher',    # Final fallback option
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher'
]
