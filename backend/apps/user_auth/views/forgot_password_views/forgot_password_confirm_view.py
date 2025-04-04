from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from limited_time_token_handler import LimitedTimeTokenDecoder

from apps.user_auth.mixins import AuthUserRateThrottleMinin
from core.views import BaseAPIView, Response

User = get_user_model()


class ForgotPasswordConfirmView(AuthUserRateThrottleMinin, BaseAPIView):
    """API view for confirming and resetting a forgotten password."""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request to confirm and reset password."""

        # Get token and new password from request
        token = request.data.get("token", "")
        new_password = request.data.get("new_password", "")

        try:
            # Decode token and get user id
            decorder = LimitedTimeTokenDecoder(token)
            if not decorder.is_valid():
                return self.handle_error(
                    "The password reset token has expired or is invalid.",
                    {
                        "token": [
                            "Invalid or expired token. Please request a new password reset."
                        ]
                    },
                )

            data = decorder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Validate and set new password
            validate_password(new_password)
            user.set_password(new_password)
            user.save()
            return self.handle_success(
                "Password successfully reset",
                {
                    "detail": "Your password has been successfully reset. You can now sign-in with your new password."
                },
            )
        except Exception as error:
            return self.handle_error(
                "An error occurred while resetting your password. Please try again.",
                {"detail": str(error)},
            )
