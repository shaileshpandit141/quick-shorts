from permissions import IsAuthenticated
from core.send_email import SendEmail
from core.views import BaseAPIView, Response
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

        # Verify password matches
        if not user.check_password(password):
            return self.handle_error(
                "Provided password is not valid.",
                [
                    {
                        "field": "password",
                        "code": "invalid_password",
                        "message": "Provided password is not valid.",
                    }
                ],
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
            "Account deactivation was successful.",
            {"detail": "Your account has been deactivated successfully."},
        )
