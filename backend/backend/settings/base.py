import os
from pathlib import Path
from datetime import timedelta  # type: ignore
from decouple import config, Csv

# Configuration Settings File for the django backend
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security Configuration Settings
# -------------------------------
SECRET_KEY = config("SECRET_KEY", cast=str)

# DEBUG Configuration Settings
# ----------------------------
DEBUG = False

# Allowed Host Configuration Settings
# -----------------------------------
ALLOWED_HOSTS = config("HOST", cast=Csv())

# Frontend URL Configuration Setting
# ----------------------------------
FRONTEND_URL = config("FRONTEND_URL", cast=str)

# Django built-in applications settings
# -------------------------------------
INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles"
]

# Third-party applications Settings
# ---------------------------------
INSTALLED_APPS += [
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "corsheaders",
]

# User Define applications Settings
# ---------------------------------
INSTALLED_APPS += [
    "users.apps.UsersConfig",
    "last_request_log.apps.LastRequestLogConfig"
]

# Middleware Configuration Settings
# ---------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "middlewares.ResponseMiddleware"
]

# Root urls file Configuration Settings
# -------------------------------------
ROOT_URLCONF = "backend.urls"

# Templates Configuration Settings
# --------------------------------
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
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Application Server Configuration Setting
# ----------------------------------------
ASGI_APPLICATION = "backend.asgi.application"

# User Model Configuration Setting
# --------------------------------
AUTH_USER_MODEL = "users.User"

# Default primary key field type Configuration Setting
# ----------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Password Validators Configuration Settings
# ------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Password hashing algorithms in order of preference
# Using multiple algorithms provides additional security layers
# -------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher"
]

# Internationalization Configuration Settings
# -------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# STATIC AND MEDIA FILES Configuration Settings
# ---------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

# Configure media files (User-uploaded files)
# -------------------------------------------
MEDIA_ROOT = BASE_DIR / "uploads"
MEDIA_URL = "/media/"

# REST Framework Configuration Settings
# -------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "permissions.IsAuthenticated"
    ],
    "EXCEPTION_HANDLER": "exceptions.exception_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
        "throttling.AuthRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/day",
        "auth": "5/hour",
        "user": "1000/day"
    },
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer"
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
}

# JWT Token Configuration Settings
# --------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=20),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=20),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Authentication Configuration Settings
# -------------------------------------
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

# EMAIL Configuration Settings
# ----------------------------
try:
    EMAIL_BACKEND = config("EMAIL_BACKEND", cast=str)
    EMAIL_HOST = config("EMAIL_HOST", cast=str)
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str)
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", cast=str, default=EMAIL_HOST_USER)
except Exception:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Logging Configuration Settings
# ------------------------------
LOGGING = {
    "version": 1,  # Version of the logging configuration
    "disable_existing_loggers": False,  # Keep default loggers like Django"s
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django.log"),
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["mail_admins", "file"],
            "level": "ERROR",
            "propagate": False,
        },
        "custom_logger": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    },
}
