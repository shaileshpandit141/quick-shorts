"""
URL Configuration for Django Backend Project

This module defines the URL patterns and routing configuration for the core Django application.
It maps URLs to their corresponding views and configures static file serving and error handling.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from .views import custom_404_apiview, IndexTemplateView
from apps.users import urls as users_urls


# Main URL patterns defining route-to-view mappings
urlpatterns = [
    # Served the index page
    path("", IndexTemplateView.as_view(), name="index"),

    # Django admin interface accessible at /admin
    path("admin/", admin.site.urls, name="admin"),

    # User authentication URLs under /api/v1/auth
    path("api/v1/auth/", include((users_urls, "auth"), namespace="auth")),
]

# Configure custom error handling
handler404 = custom_404_apiview

# Enable serving of user-uploaded media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
