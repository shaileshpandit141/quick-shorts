from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user_auth.mixins import IsUserAuthenticatedPermissionsMixin

User = get_user_model()


class ChangePasswordView(IsUserAuthenticatedPermissionsMixin, APIView):
    """Changes authenticated user's password."""

    def post(self, request, *args, **kwargs) -> Response:
        """Changes user password after validation."""

        # Get required data from request
        user = request.user
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("old_password", "")

        # Check if old password is correct
        if not user.check_password(old_password):
            return failure_response(
                message="Invalid Password",
                errors={"password": ["The password you entered is incorrect."]},
            )

        # Validate new password complexity
        try:
            validate_password(new_password)
        except Exception as _:
            return failure_response(
                message="Password Requirements Not Met",
                errors={
                    "password": ["Password validation failed. Change entered password."]
                },
            )

        # Set new password and notify user via email
        user.set_password(new_password)
        user.save()

        # Handel email send
        email = EmailService(
            subject="Password Change Notification",
            emails=Emails(
                from_email=None,
                to_emails=[user.email],
            ),
            context={"user": user},
            templates=Templates(
                text_template="users/change_password/success_message.txt",
                html_template="users/change_password/success_message.html",
            ),
        )

        # Send password changed success email
        email.send(fallback=False)

        # Return success response
        return success_response(
            message="Password Changed Successfully",
            data={"detail": "Your password has been updated successfully."},
        )
