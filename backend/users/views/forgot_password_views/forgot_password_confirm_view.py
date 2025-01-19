# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Local imports
from permissions import AllowAny
from throttling import AuthRateThrottle
from utils import FieldValidator
from quick_utils.token_generator import TokenGenerator
from quick_utils.views import QuickAPIView, Response

User = get_user_model()


class ForgotPasswordConfirmView(QuickAPIView):
    """API view for confirming and resetting a forgotten password."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request to confirm and reset password."""

        # Validate required fields
        clean_data = FieldValidator(request.data, [
            "token",
            "token_salt",
            "new_password"
        ])
        if not clean_data.is_valid():
            return self.response({
                "message": "Invalid request",
                "errors": clean_data.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        try:
            # Decode token and get user
            data = TokenGenerator.decode(
                clean_data.get("token"),
                clean_data.get("token_salt")
            )
            user = User.objects.get(id=data["user_id"])

            # Validate and set new password
            validate_password(clean_data.get("new_password"))
            user.set_password(clean_data.get("new_password"))
            user.save()

            return self.response({
                "message": "Password changed successfully",
                "data": {
                    "detail": "Your password has been successfully updated"
                }
            }, self.status.HTTP_200_OK)

        except Exception as error:
            return self.response({
                "message": "Invalid request",
                "errors": [{
                    "field": "none",
                    "code": "invalid_request",
                    "message": str(error),
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)
