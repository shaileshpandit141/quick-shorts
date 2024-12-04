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
    UserRegisterAPIView,
    SigninTokenObtainPairAPIView,
    SigninTokenRefreshAPIView,
    EmailVerificationAPIView,
    # CustomResendVerificationEmailView,
    UserInfoView
)

urlpatterns = [
    # Authentication endpoints for user registration and logout
    path("signup/", UserRegisterAPIView.as_view(), name="account_signup"),
    path("token/", SigninTokenObtainPairAPIView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", SigninTokenRefreshAPIView.as_view(), name="token_refresh"),
    path('email-verification/', EmailVerificationAPIView.as_view(), name='email_verification'),
    # path(
    #     "signup/resend-verification-email/",
    #     CustomResendVerificationEmailView.as_view(),
    #     name="account_resend_email_verification"
    # ),

    # User data endpoints for profile information
    path("user/", UserInfoView.as_view(), name="user")
]
