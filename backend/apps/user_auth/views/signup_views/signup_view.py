from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from dns_smtp_email_validator import DNSSMTPEmailValidator
from limited_time_token_handler import LimitedTimeTokenGenerator
from user_auth.serializers import UserSerializer

from apps.user_auth.mixins import AuthUserRateThrottleMinin
from core.send_email import SendEmail
from core.views import BaseAPIView, Response

User = get_user_model()


class SignupView(AuthUserRateThrottleMinin, BaseAPIView):
    """API view for handling user signup functionality"""

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user registration"""

        # Gatting submitted data from request
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        confirm_password = request.data.get("confirm_password", None)
        active_url = request.data.get("active_url", None)

        # Handle if user not include email in payload
        if email is None:
            return self.handle_error(
                "Sign up failed",
                {"email": ["Please provide a valid email address."]},
            )

        # Handle if user not include password in payload
        if password is None:
            return self.handle_error(
                "Sign up failed",
                {"password": ["Please provide a password."]},
            )

        # Handle if user not include password in payload
        if confirm_password is None:
            return self.handle_error(
                "Sign up failed",
                {"confirm_password": ["Please confirm your password."]},
            )

        try:
            # Validate password meets requirements
            validate_password(password)
        except ValidationError:
            return self.handle_error(
                "Invalid password",
                {
                    "password": [
                        "Password must be at least 8 characters long and contain a mix of letters, numbers and symbols."
                    ]
                },
            )

        # Check password confirmation matches
        if password != confirm_password:
            return self.handle_error(
                "Password mismatch",
                {"confirm_password": ["Passwords do not match. Please try again."]},
            )

        # Validate the email is exist in the internet or not
        validator = DNSSMTPEmailValidator(email)
        if not validator.is_valid():
            return self.handle_error(
                "Invalid email domain",
                {
                    "email": [
                        "The email domain appears to be invalid. Please use a valid email address."
                    ]
                },
            )

        # Hash the password for secure storage
        hashed_password = make_password(password)

        # Create new user instance
        serializer = UserSerializer(
            data={"email": email},
            context={"hashed_password": hashed_password},
        )

        # Check serialize is valid or not
        if not serializer.is_valid():
            return self.handle_error(
                "Sign up failed",
                serializer.errors,
            )

        # Save serializer data if it valid
        serializer.save()
        user = serializer.instance

        # Generate verification token and URL
        generator = LimitedTimeTokenGenerator({"user_id": getattr(user, "id")})
        token = generator.generate()
        if token is None:
            return self.handle_error(
                "Verification token generation failed",
                {
                    "detail": "Unable to generate verification token. Please try registering again."
                },
            )

        # Send verification email
        SendEmail(
            {
                "subject": "Verify Your Account",
                "emails": {"to_emails": [getattr(user, "email", "Unknown")]},
                "context": {"user": user, "activate_url": f"{active_url}/{token}"},
                "templates": {
                    "txt": "users/verify_account/confirm_message.txt",
                    "html": "users/verify_account/confirm_message.html",
                },
            }
        )

        # Return success response object
        return self.handle_success(
            "Sign up successful",
            {"detail": "Success! Please check your email to verify your account."},
        )
