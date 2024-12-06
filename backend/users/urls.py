'''
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.
'''

from django.urls import path
from .views import (
    GenerateEmailVerificationLinkAPIView,
    ChangePasswordAPIView,
    SigninTokenAPIView,
    SigninTokenRefreshAPIView,
    SignupAPIView,
    UserInfoAPIView,
    VerifyEmailAPIView,
)

urlpatterns = [
    path(
        'generate-email-verification-link/',
        GenerateEmailVerificationLinkAPIView.as_view(),
        name='generate-email-verification-link'
    ),
    path('token/', SigninTokenAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', SigninTokenRefreshAPIView.as_view(), name='token_refresh'),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),

    # User data endpoints for profile information
    path('user/', UserInfoAPIView.as_view(), name='user'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify_email')
]
