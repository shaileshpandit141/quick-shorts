# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings

# Local imports
from quick_utils.views import QuickAPIView, Response
from permissions import AllowAny
from throttling import AuthRateThrottle
from utils import (
    SendEmail,
    TokenGenerator,
    add_query_params,
    FieldValidator
)

User = get_user_model()


class VerifyAccountView(QuickAPIView):
    """API View for handling account verification."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Process a request to resend an account verification email."""

        # Validate required email field
        clean_data = FieldValidator(request.data, ["email"])

        if not clean_data.is_valid():
            return self.response({
                "message": "Please provide a valid email address",
                "errors": clean_data.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=clean_data.get("email"))
        except User.DoesNotExist:
            return self.response({
                "message": "User account not found",
                "errors": [{
                    "field": "email",
                    "code": "not_exist",
                    "message": "We could not find an account with this email address",
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        if not user.is_verified:
            # Generate verification token and URL
            payload = TokenGenerator.generate({"user_id": user.id})
            activate_url = add_query_params(f"{settings.FRONTEND_URL}/auth/verify-email", {
                "token": payload["token"],
                "token_salt": payload["token_salt"]
            })

            # Send verification email
            SendEmail({
                "subject": "Account Verification Request",
                "emails": {
                    "to_emails": [clean_data.get("email")]
                },
                "context": {
                    "user": user,
                    "activate_url": activate_url
                },
                "templates": {
                    "txt": "users/verify_account/confirm_message.txt",
                    "html": "users/verify_account/confirm_message.html"
                }
            })
            return self.response({
                "message": "Account Verification email sent successfully",
                "data": {
                    "detail": """We have sent a Account verification link to your email.
                    Please check your inbox to complete the verification process."""
                }
            }, self.status.HTTP_200_OK)
        else:
            return self.response({
                "message": "Account already verified",
                "data": {
                    "detail": "This Account has already been verified. You can proceed to sign in."
                }
            }, self.status.HTTP_200_OK)
