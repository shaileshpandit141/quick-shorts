"""
Django settings for the backend project.

This module contains the configuration settings for the Django backend project, including:
- Core Django settings
- Database configuration
- Authentication settings
- Static/Media files handling
- REST framework configuration
- JWT settings
- Email configuration
- Security settings

For more details on Django settings see:
https://docs.djangoproject.com/en/5.0/topics/settings/
"""

from pathlib import Path
from datetime import timedelta
from decouple import config, Csv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR points to the root directory containing manage.py
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY SETTINGS
# ----------------
SECRET_KEY = config("SECRET_KEY")  # Django secret key from env
DEBUG = config("DEBUG", cast=bool, default=False)  # Debug mode setting
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())  # Allowed host domains
APPEND_SLASH = False  # Don't append slashes to URLs

# FRONTEND URL SETTINGS
# ----------------
FRONTEND_URL = config("FRONTEND_URL", cast=str)

# APPLICATION CONFIGURATION
# -----------------------
INSTALLED_APPS = [
    "daphne",  # ASGI server
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# Third-party applications
INSTALLED_APPS += [
    "rest_framework",  # REST API
    "rest_framework.authtoken",
    "rest_framework_simplejwt",  # JWT authentication
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",  # CORS handling
]

# Local applications
INSTALLED_APPS += [
    "users.apps.UsersConfig",
]

# MIDDLEWARE CONFIGURATION
# ----------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

# URL AND TEMPLATE CONFIGURATION
# ----------------------------
ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages"
            ],
        },
    },
]

# APPLICATION SERVER
# ----------------
ASGI_APPLICATION = "backend.asgi.application"

# USER MODEL AND DATABASE
# ----------------------
AUTH_USER_MODEL = 'users.User'  # Custom user model
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# SQLite database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Postgresql configuration (commented out)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DB_NAME'),
#         'USER': config('DB_USER'),
#         'PASSWORD': config('DB_PASSWORD'),
#         'HOST': config('DB_HOST', default='localhost'),
#         'PORT': config('DB_PORT', default='5432'),
#     }
# }

# PASSWORD VALIDATION
# -----------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# INTERNATIONALIZATION
# ------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# STATIC AND MEDIA FILES
# ---------------------
STATIC_URL = "/static/"  # URL prefix for static files
STATIC_ROOT = BASE_DIR / "staticfiles"  # Collected static files directory
STATICFILES_DIRS = [BASE_DIR / "static"]  # Additional static file locations

MEDIA_ROOT = BASE_DIR / "uploads"  # User uploaded files directory
MEDIA_URL = "/media/"  # URL prefix for media files

# REST FRAMEWORK SETTINGS
# ---------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated",],
    "DEFAULT_PERMISSION_CLASSES": ["permissions.IsAuthenticated",],
    'EXCEPTION_HANDLER': 'backend.exceptions.custom_exception_handler',
    "DEFAULT_THROTTLE_CLASSES": [
        # "rest_framework.throttling.AnonRateThrottle",
        # "rest_framework.throttling.UserRateThrottle",
        "throttles.AnonRateThrottle",
        "throttles.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",  # Rate limit for anonymous users
        "user": "1000/day",  # Rate limit for authenticated users
    },
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}

# JWT CONFIGURATION
# ---------------
REST_USE_JWT = True
JWT_AUTH_HEADER_PREFIX = 'Bearer'

# JWT TOKEN SETTINGS
# ----------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# AUTHENTICATION SETTINGS
# ---------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# EMAIL SETTINGS
# ------------
EMAIL_BACKEND = config("EMAIL_BACKEND", cast=str)
EMAIL_HOST = config("EMAIL_HOST", cast=str)
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
DEFAULT_FROM_EMAIL = config(
    "DEFAULT_FROM_EMAIL", cast=str, default=config("EMAIL_HOST_USER")
)
