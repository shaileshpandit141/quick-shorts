'''
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.
'''

from django.urls import path
from .views import (
    SignupAPIView,
    SigninTokenAPIView,
    SigninTokenRefreshAPIView,
    SignoutAPIView,
    VerifyEmailAPIView,
    VerifyEmailConfirmAPIView,
    ChangePasswordAPIView,
    ForgotPasswordAPIView,
    ForgotPasswordConfirmAPIView,
    DeactivateAccountAPIView,
    UserInfoAPIView,
)

urlpatterns = [
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('signin/token/', SigninTokenAPIView.as_view(), name='signin_token'),
    path('signin/token/refresh/', SigninTokenRefreshAPIView.as_view(), name='signin_token_refresh'),
    path('signout/', SignoutAPIView.as_view(), name='sign_out'),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify_email'),
    path('verify-email-confirm/', VerifyEmailConfirmAPIView.as_view(), name='verify_email_confirm'),
    path('change-pasaword/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('forgot-password-confirm/', ForgotPasswordConfirmAPIView.as_view(), name='forgot_password_confirm'),
    path('deactivate-account/', DeactivateAccountAPIView.as_view(), name='deactivate_account'),
    path('user/', UserInfoAPIView.as_view(), name='user-info'),
]
