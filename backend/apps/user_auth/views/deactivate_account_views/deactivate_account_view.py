from rest_core.email_service import Emails, EmailService, Templates
from rest_core.response import failure_response, success_response
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user_auth.mixins import IsUserAuthenticatedPermissionsMixin


class DeactivateAccountView(IsUserAuthenticatedPermissionsMixin, APIView):
    """API view for deactivating user accounts."""

    def post(self, request, *args, **kwargs) -> Response:
        """Deactivate the authenticated user's account."""

        # Get user and password from request
        user = request.user
        password = request.data.get("password", None)

        # Handle if password is blank
        if password is None:
            return failure_response(
                message="Password is required to deactivate your account",
                errors={
                    "password": [
                        "Please enter your password to confirm account deactivation."
                    ]
                },
            )

        # Verify password matches
        if not user.check_password(password):
            return failure_response(
                message="Incorrect password provided",
                errors={
                    "password": [
                        "The password you entered is incorrect. Please try again."
                    ]
                },
            )

        # Deactivate the account
        user.is_active = False
        user.save()

        # Handel email send
        email = EmailService(
            subject="Account Deactivation Confirmation",
            emails=Emails(
                from_email=None,
                to_emails=[user.email],
            ),
            context={"user": user},
            templates=Templates(
                text_template="users/deactivate_account/confirm_message.txt",
                html_template="users/deactivate_account/confirm_message.html",
            ),
        )

        # Send deactivation confirmation email
        email.send(fallback=False)

        # Return success response
        return success_response(
            message="Account deactivated successfully",
            data={
                "detail": "Your account has been deactivated. You will be signed out shortly."
            },
        )
