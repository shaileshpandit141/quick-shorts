from apps.user_auth.mixins import IsUserAuthenticatedPermissionsMixin
from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class ChangePasswordView(IsUserAuthenticatedPermissionsMixin, BaseAPIView):
    """Changes authenticated user's password."""

    def post(self, request, *args, **kwargs) -> Response:
        """Changes user password after validation."""

        user = request.user
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("old_password", "")

        # Check if old password is correct
        if not user.check_password(old_password):
            return self.handle_error(
                "Invalid Password",
                {"detail": "The password you entered is incorrect. Please try again."},
            )

        # Validate new password complexity
        try:
            validate_password(new_password)
        except Exception as error:
            return self.handle_error(
                "Password Requirements Not Met",
                {"detail": f"Password validation failed: {str(error)}"},
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
            "Password Changed Successfully",
            {
                "detail": "Your password has been updated successfully. You can now use your new password to sign in."
            },
        )
