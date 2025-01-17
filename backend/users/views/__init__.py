from .change_password_views import ChangePasswordView
from .deactivate_account_views import DeactivateAccountView
from .forgot_password_views import ForgotPasswordView, ForgotPasswordConfirmView
from .signin_token_views import SigninTokenView, SigninTokenRefreshView
from .signout_views import SignoutView
from .signup_views import SignupView
from .user_info_views import UserInfoView
from .verify_account_views import VerifyAccountView, VerifyAccountConfirmView

__all__ = [
    'ChangePasswordView',
    'DeactivateAccountView',
    'ForgotPasswordView',
    'ForgotPasswordConfirmView',
    'SigninTokenView',
    'SigninTokenRefreshView',
    'SignoutView',
    'SignupView',
    'UserInfoView',
    'VerifyAccountView',
    'VerifyAccountConfirmView'
]
