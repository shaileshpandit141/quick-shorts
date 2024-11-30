"""
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.

Available Endpoints:
    Authentication:
        signup/ - New user registration
        signout/ - User logout
        token/ - Obtain JWT authentication tokens
        token/refresh/ - Refresh expired JWT access token

    Email Verification:
        signup/verify-email/ - Verify email after registration
        signup/resend-email-verification/ - Resend verification email

    Password Management:
        password/reset/ - Initiate password reset process
        password/reset/confirm/ - Process reset token
        password/reset/confirm/<uidb64>/<token>/ - Complete reset with token

    User Data:
        user/ - Retrieve authenticated user details
"""

from django.urls import path
from .views import (
    CustomRegisterView,
    CustomLogoutView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomVerifyEmailView,
    CustomResendVerificationEmailView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    UserInfoView
)

urlpatterns = [
    # Authentication endpoints for user registration and logout
    path("signup/", CustomRegisterView.as_view(), name="account_signup"),
    path("signout/", CustomLogoutView.as_view(), name="custom_logout"),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),

    # Email verification endpoints for account confirmation
    path(
        "signup/verify-email/",
        CustomVerifyEmailView.as_view(),
        name="account_email_verification_sent"
    ),
    path(
        "signup/resend-verification-email/",
        CustomResendVerificationEmailView.as_view(),
        name="account_resend_email_verification"
    ),

    # Password management endpoints for reset workflow
    path(
        "password/reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset"
    ),
    path(
        "password/reset/confirm/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),
    path(
        "password/reset/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm"
    ),

    # User data endpoints for profile information
    path("user/", UserInfoView.as_view(), name="user")
]
