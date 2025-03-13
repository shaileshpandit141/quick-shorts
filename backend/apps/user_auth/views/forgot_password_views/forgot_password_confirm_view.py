from core.views import BaseAPIView, Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from limited_time_token_handler import LimitedTimeTokenDecoder
from permissions import AllowAny
from throttling import AuthRateThrottle

User = get_user_model()


class ForgotPasswordConfirmView(BaseAPIView):
    """API view for confirming and resetting a forgotten password."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

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
                    "Provided toke is expired or invalid.",
                    {"token": ["Token is invalid or expired, request a new one."]},
                )

            data = decorder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Validate and set new password
            validate_password(new_password)
            user.set_password(new_password)
            user.save()
            return self.handle_success(
                "Your password changed successfull",
                {"detail": "Your password has been successfully updated"},
            )
        except Exception as error:
            return self.handle_error(
                "Opp's! somethings want wrong. Please try again later.",
                {"detail": str(error)},
            )
