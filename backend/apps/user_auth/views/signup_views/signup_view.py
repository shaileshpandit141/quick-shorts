from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from dns_smtp_email_validator import DNSSMTPEmailValidator
from limited_time_token_handler import LimitedTimeTokenGenerator
from permissions import AllowAny
from core.send_email import SendEmail
from core.views import BaseAPIView, Response
from throttling import AuthRateThrottle
from user_auth.serializers import UserSerializer

User = get_user_model()


class SignupView(BaseAPIView):
    """API view for handling user signup functionality"""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user registration"""

        email = request.data.get("email", "")
        password = request.data.get("password", "")
        confirm_password = request.data.get("confirm_password", "")

        try:
            # Validate password meets requirements
            validate_password(password)
        except ValidationError as error:
            return self.handle_error(
                "Provided password is not valid.",
                [
                    {
                        "field": "password",
                        "code": "invalid_password",
                        "message": str(error),
                    }
                ],
            )

        # Check password confirmation matches
        if password != confirm_password:
            return self.handle_error(
                "Confirm password is not equal to password.",
                [
                    {
                        "field": "confirm_password",
                        "code": "confirm_password_not_metch",
                        "message": "Confirm password is not equal to password.",
                    }
                ],
            )

        # Validate the email is exist in the internet or not
        validator = DNSSMTPEmailValidator(email)
        if not validator.is_valid():
            return self.handle_error(
                "Email validation failed.",
                [
                    {
                        "field": "email",
                        "code": "invalid_email",
                        "message": "Email validation failed. Please try again later.",
                    }
                ],
            )

        # Hash the password for secure storage
        hashed_password = make_password(password)

        # Create new user instance
        serializer = UserSerializer(
            data={"email": email},
            context={"hashed_password": hashed_password},
        )
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance

            # Generate verification token and URL
            generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
            token = generator.generate()
            if token is None:
                return self.handle_error(
                    "Filed to generate an account verification token.",
                    [
                        {
                            "field": "token",
                            "code": "token_generation_failed",
                            "message": "We couldn't generate an account verification token. Please try again later.",
                        }
                    ],
                )

            activate_url = f"{settings.FRONTEND_URL}/auth/verify-user-account/{token}"
            # Send verification email
            SendEmail(
                {
                    "subject": "For Account Verification",
                    "emails": {"to_emails": [getattr(user, "email", "Unknown")]},
                    "context": {"user": user, "activate_url": activate_url},
                    "templates": {
                        "txt": "users/verify_account/confirm_message.txt",
                        "html": "users/verify_account/confirm_message.html",
                    },
                }
            )
            return self.handle_success(
                "Sign up request was successful.",
                {"detail": "Please check your inbox for the account verification."},
            )
        return self.handle_error(
            "Provided data is not valid.",
            self.format_serializer_errors(serializer.errors),
        )
