"""
Django Accounts App URL Configuration

This module defines URL patterns for the accounts application, handling user authentication,
registration, password management, and profile data. All paths are prefixed with /accounts/
when included in the main URLs.
"""

from django.urls import path

from .views.change_password_views import ChangePasswordView
from .views.deactivate_account_views import DeactivateAccountView
from .views.reset_password_views import ResetPasswordConfirmView, ResetPasswordView
from .views.signin_token_views import SigninTokenRefreshView, SigninTokenView
from .views.signout_views import SignoutView
from .views.signup_views import SignupView
from .views.user_info_views import UserInfoView
from .views.verify_account_views import VerifyAccountConfirmView, VerifyAccountView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("signin/token/", SigninTokenView.as_view(), name="signin-token"),
    path(
        "signin/token/refresh/",
        SigninTokenRefreshView.as_view(),
        name="signin-token-refresh",
    ),
    path("signout/", SignoutView.as_view(), name="signout"),
    path("verify-account/", VerifyAccountView.as_view(), name="verify-account"),
    path(
        "verify-account/confirm/",
        VerifyAccountConfirmView.as_view(),
        name="verify-account-confirm",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset-password"),
    path(
        "reset-password/confirm/",
        ResetPasswordConfirmView.as_view(),
        name="reset-password-confirm",
    ),
    path(
        "deactivate-account/",
        DeactivateAccountView.as_view(),
        name="deactivate-account",
    ),
    path("user/", UserInfoView.as_view(), name="user-info"),
]
