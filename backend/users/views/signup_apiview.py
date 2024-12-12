# Django imports
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import (
    Response,
    SendEmail,
    TokenGenerator,
    add_query_params,
    FieldValidator
)
from users.serializers import UserSerializer

User = get_user_model()


class SignupAPIView(APIView):
    """
    API view for handling user signup functionality.
    Allows new users to register and sends email verification.
    """

    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """Disallow GET method"""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Handle user registration:
        1. Validate required fields (email, password, confirm_password)
        2. Validate and hash password
        3. Create new user
        4. Send verification email

        Returns:
            Success response with verification email status or
            Error response with validation errors
        """
        # Validate required fields
        clean_data = FieldValidator(request.data, [
            'email',
            'password',
            'confirm_password'
        ])

        if not clean_data.is_valid():
            return Response.error({
                'message': 'Validation error',
                'errors': clean_data.get_errors()
            }, status=status.HTTP_400_BAD_REQUEST)

        password = clean_data.get('password')
        confirm_password = clean_data.get('confirm_password')

        # Validate password meets requirements
        try:
            validate_password(password)
        except ValidationError as error:
            return Response.error({
                'message': 'Invalid password',
                'errors': {
                    'password': [str(error)]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check password confirmation matches
        if password != confirm_password:
            return Response.error({
                'message': 'Validation error',
                'errors': {
                    'confirm_password': ['Confirm password is not equal to password']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

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

            return Response.success({
                'message': 'Verification email sent',
                'data': {
                    'detail': 'Please check your inbox for the email verification'
                }
            }, status=status.HTTP_200_OK)

        return Response.error({
            'message': 'Invalid data provided',
            'errors': serializer.errors  # type: ignore
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        """Disallow PUT method"""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """Disallow PATCH method"""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """Disallow DELETE method"""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
