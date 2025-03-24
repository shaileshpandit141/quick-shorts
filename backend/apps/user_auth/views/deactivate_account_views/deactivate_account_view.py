from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from permissions import IsAuthenticated
from throttling import UserRateThrottle


class DeactivateAccountView(BaseAPIView):
    """API view for deactivating user accounts."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Deactivate the authenticated user's account."""

        # Get user and password from request
        user = request.user
        password = request.data.get("password", None)

        # Handle if password is blank
        if password is None:
            return self.handle_error(
                "Password is required to deactivate your account",
                {
                    "password": [
                        "Please enter your password to confirm account deactivation."
                    ]
                },
            )

        # Verify password matches
        if not user.check_password(password):
            return self.handle_error(
                "Incorrect password provided",
                {
                    "password": [
                        "The password you entered is incorrect. Please try again."
                    ]
                },
            )

        # Deactivate the account
        user.is_active = False
        user.save()

        # Send confirmation email
        SendEmail(
            {
                "subject": "Account Deactivation Confirmation",
                "emails": {"to_emails": [user.email]},
                "context": {"user": user},
                "templates": {
                    "txt": "users/deactivate_account/confirm_message.txt",
                    "html": "users/deactivate_account/confirm_message.html",
                },
            }
        )

        return self.handle_success(
            "Account deactivated successfully",
            {
                "detail": "Your account has been deactivated. You will be signed out shortly."
            },
        )
