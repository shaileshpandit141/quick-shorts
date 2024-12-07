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
from utils import Response, SendEmail, TokenGenerator, add_query_params
from users.serializers import UserSerializer

User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        # Extract the password from request data
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)

        # Check if the password and confirm_password is provided or not
        if email is None or password is None or confirm_password is None:
            errors = {}
            if email is None:
                errors['email'] = ['Email field is required']
            elif User.objects.filter(email=email).exists():
                errors['email'] = ['User with this email already exists.']
                return Response.error({
                    'message': 'Validation error',
                    'errors': errors
                }, status=status.HTTP_400_BAD_REQUEST)
            if password is None:
                errors['password'] = ['Password field is required']
            if confirm_password is None:
                errors['confirm_password'] = ['Confirm password field is required']

            return Response.error({
                'message': 'Validation error',
                'errors': errors
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate the password
        try:
            validate_password(password)
        except ValidationError as error:
            return Response.error({
                'message': 'Invalid password',
                'errors': {
                    'password': [str(error)]
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response.error({
                'message': 'Validation error',
                'errors': {
                    'confirm_password': ['Confirm password is not equal to password']
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Hash the password
        hashed_password = make_password(password)

        # Serialize and validate the data
        serializer = UserSerializer(
            data=request.data,
            context={'hashed_password': hashed_password}
        )
        if serializer.is_valid():
            serializer.save()
            user = serializer.instance
            # Generate token
            payload = TokenGenerator.generate({"user_id": user.id}) # type: ignore
            activate_url = add_query_params(f'{settings.FRONTEND_URL}/auth/verify-email', {
                'token': payload['token'],
                'token_salt': payload['token_salt']
            })

            SendEmail({
                'subject': 'For email verification',
                'emails': {
                    'to_emails': user.email # type: ignore
                },
                'context': {
                    'user': user,
                    'activate_url': activate_url
                },
                'templates': {
                    'txt': 'users/email_verification_message.txt',
                    'html': 'users/email_verification_message.html'
                }
            })

            return Response.success({
                'message': 'Verification email sent',
                'data': {
                    'detail': 'Please check your inbox for the email verification'
                }
            }, status=status.HTTP_200_OK)

        # Return errors if serializer is invalid
        return Response.error({
            'message': 'Invalid data provided',
            'errors': serializer.errors  # type: ignore
        }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])
