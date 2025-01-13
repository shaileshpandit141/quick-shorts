# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

# Import the DNSSMTPEmailValidator
from dns_smtp_email_validator import DNSSMTPEmailValidator

# Local imports
from quick_utils.views import QuickAPIView, Response
from permissions import AllowAny
from throttling import AnonRateThrottle
from utils import (
    SendEmail,
    TokenGenerator,
    add_query_params,
    FieldValidator
)
from users.serializers import UserSerializer

User = get_user_model()


class SignupAPIView(QuickAPIView):
    """API view for handling user signup functionality"""

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle user registration"""

        # Validate required fields
        clean_data = FieldValidator(request.data, [
            "email",
            "password",
            "confirm_password"
        ])

        if not clean_data.is_valid():
            return self.error_response({
                "message": "Validation error",
                "errors": clean_data.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        email = clean_data.get("email")
        password = clean_data.get("password")
        confirm_password = clean_data.get("confirm_password")

        # Validate password meets requirements
        try:
            validate_password(password)
        except ValidationError as error:
            return self.error_response({
                "message": "Validation error",
                "errors": [{
                    "field": "password",
                    "code": "invalid_password",
                    "message": error[0] if isinstance(error, list) else str(error),
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        # Check password confirmation matches
        if password != confirm_password:
            return self.error_response({
                "message": "Validation error",
                "errors": [{
                    "field": "none",
                    "code": "confirm_password_not_metch",
                    "message": "Confirm password is not equal to password",
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        # Validate the email is exist in the internet or not
        validator = DNSSMTPEmailValidator(email)
        if not validator.is_valid():
            return self.error_response({
                "message": "Email Validation Failed",
                "errors": validator.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        # Hash the password for secure storage
        hashed_password = make_password(password)

        # Create new user instance
        serializer = UserSerializer(
            data=clean_data.data,
            context={'hashed_password': hashed_password}
        )
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance

            # Generate verification token and URL
            payload = TokenGenerator.generate({"user_id": user.id}) # type: ignore
            activate_url = add_query_params(f'{settings.FRONTEND_URL}/auth/verify-email', {
                'token': payload['token'],
                'token_salt': payload['token_salt']
            })

            # Send verification email
            SendEmail({
                'subject': 'For email verification',
                'emails': {
                    'to_emails': [user.email] # type: ignore
                },
                'context': {
                    'user': user,
                    'activate_url': activate_url
                },
                'templates': {
                    'txt': 'users/verify_account/confirm_message.txt',
                    'html': 'users/verify_account/confirm_message.html'
                }
            })

            return self.success_response({
                "message": "Sign up Successful",
                "data": {
                    "detail": "Please check your inbox for the email verification"
                }
            }, self.status.HTTP_200_OK)

        return self.error_response({
            'message': 'Invalid data provided',
            'errors': self.format_serializer_errors(serializer.errors)
        }, self.status.HTTP_400_BAD_REQUEST)
