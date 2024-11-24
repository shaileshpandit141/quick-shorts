"""
URL Configuration for Django Accounts App

This module defines URL patterns for account-related functionalities. All paths are
prefixed with /accounts/ when included in the main URL configuration.

Authentication Routes:
    /auth/signup/ - User registration
    /auth/signup/verify-email/ - Email verification after signup
    /auth/signup/resend-email-verification/ - Resend verification email
    /auth/signout/ - User logout

Password Management:
    /auth/password/reset/ - Initiate password reset
    /auth/password/reset/confirm/ - Handle password reset token
    /auth/password/reset/confirm/<uidb64>/<token>/ - Complete password reset

Token Management:
    /auth/token/ - Obtain JWT token pair
    /auth/token/refresh/ - Refresh expired access token

User Data:
    /user/ - Get authenticated user information
    /protected/ - Example protected endpoint requiring authentication
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from dj_rest_auth.views import PasswordResetConfirmView
from dj_rest_auth.registration.views import (
    RegisterView,
    VerifyEmailView
)
from .views import (
    CustomPasswordResetView,
    ResendVerificationEmailView,
    CustomSignoutView,
    CustomTokenObtainPairView,
    UserInfoView,
    ProtectedView,
)

urlpatterns = [
    # Authentication endpoints for user registration and verification
    path("signup/", RegisterView.as_view(), name="account_signup"),
    path("signup/verify-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    path("signup/resend-email-verification/", ResendVerificationEmailView.as_view(), name="account_resend_email_verification"),
    path("signout/", CustomSignoutView.as_view(), name="custom_logout"),

    # Password reset flow endpoints
    path("password/reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/confirm/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    # JWT token endpoints for authentication
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # User data and protected endpoints requiring authentication
    path("user/", UserInfoView.as_view(), name="user"),
    path("protected/", ProtectedView.as_view(), name="protected"),
]
