from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from limited_time_token_handler import LimitedTimeTokenDecoder
from permissions import AllowAny
from quick_utils.views import APIView, Response
from throttling import AuthRateThrottle
from utils import FieldValidator

User = get_user_model()


class ForgotPasswordConfirmView(APIView):
    """API view for confirming and resetting a forgotten password."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request to confirm and reset password."""

        # Validate required fields
        clean_data = FieldValidator(request.data, ["token", "new_password"])
        if not clean_data.is_valid():
            return self.response(
                {"message": "Invalid request", "errors": clean_data.errors},
                self.status.HTTP_400_BAD_REQUEST,
            )

        try:
            # Decode token and get user
            decorder = LimitedTimeTokenDecoder(clean_data.get("token"))
            if not decorder.is_valid():
                return self.response(
                    {
                        "message": "Invalid request",
                        "errors": [
                            {
                                "field": "token",
                                "code": "invalid_token",
                                "message": "Token is invalid or expired, request a new one",
                                "details": None,
                            }
                        ],
                    },
                    self.status.HTTP_400_BAD_REQUEST,
                )

            data = decorder.decode()
            user = User.objects.get(id=data.get("user_id"))

            # Validate and set new password
            validate_password(clean_data.get("new_password"))
            user.set_password(clean_data.get("new_password"))
            user.save()

            return self.response(
                {
                    "message": "Password changed successfully",
                    "data": {"detail": "Your password has been successfully updated"},
                },
                self.status.HTTP_200_OK,
            )

        except Exception as error:
            return self.response(
                {
                    "message": "An error occurred while processing your request. Please try again later.",
                    "errors": [
                        {
                            "field": "none",
                            "code": type(error).__name__,
                            "message": "We encountered an unexpected issue. Please try again.",
                            "details": {"detail": str(error)},
                        }
                    ],
                },
                self.status.HTTP_400_BAD_REQUEST,
            )
