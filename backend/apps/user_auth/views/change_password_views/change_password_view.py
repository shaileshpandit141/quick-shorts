from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from permissions import IsAuthenticated
from throttling import AuthRateThrottle

User = get_user_model()


class ChangePasswordView(BaseAPIView):
    """Changes authenticated user's password."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Changes user password after validation."""

        user = request.user
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("old_password", "")

        # Check if old password is correct
        if not user.check_password(old_password):
            return self.handle_error(
                "The old password you entered is incorrect",
                {"detail": "Please enter your current password correctly."},
            )

        # Validate new password complexity
        try:
            validate_password(new_password)
        except Exception as error:
            return self.handle_error(
                "Your new password does not meet the requirements",
                {"detail": str(error)},
            )

        # Set new password and notify user via email
        user.set_password(new_password)
        user.save()
        SendEmail(
            {
                "subject": "Password Change Notification",
                "emails": {"to_emails": [user.email]},
                "context": {"user": user},
                "templates": {
                    "txt": "users/change_password/success_message.txt",
                    "html": "users/change_password/success_message.html",
                },
            }
        )

        return self.handle_success(
            "Password updated successfully",
            {"detail": "Your password has been changed."},
        )
