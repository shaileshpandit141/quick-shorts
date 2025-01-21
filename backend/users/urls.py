"""
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.
"""

from django.urls import path
from .views import (
    SignupView,
    SigninTokenView,
    SigninTokenRefreshView,
    SignoutView,
    VerifyAccountView,
    VerifyAccountConfirmView,
    ChangePasswordView,
    ForgotPasswordView,
    ForgotPasswordConfirmView,
    DeactivateAccountView,
    UserInfoView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/token/", SigninTokenView.as_view(), name="signin_token"),
    path("signin/token/refresh/", SigninTokenRefreshView.as_view(), name="signin_token_refresh"),
    path("signout/", SignoutView.as_view(), name="sign_out"),
    path("verify-account/", VerifyAccountView.as_view(), name="verify_acccount"),
    path("verify-account/confirm/", VerifyAccountConfirmView.as_view(), name="verify_acccount_confirm"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot_password"),
    path("forgot-password/confirm/", ForgotPasswordConfirmView.as_view(), name="forgot_password_confirm"),
    path("deactivate-account/", DeactivateAccountView.as_view(), name="deactivate_account"),
    path("user/", UserInfoView.as_view(), name="user-info"),
]
