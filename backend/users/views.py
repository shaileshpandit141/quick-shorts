# Django imports
from django.contrib.auth import get_user_model
from django.utils import timezone

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# REST framework SimpleJWT imports
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

# Local imports
from permissions import AllowAny, IsAuthenticated, IsEmailVerified
from throttles import AnonRateThrottle, UserRateThrottle
from utils import Response, SendEmail, TokenGenerator
from .serializers import UserSerializer, SigninTokenObtainPairSerializer


User = get_user_model()


class SignupAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('get')

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
            id = user.id  # type: ignore
            email = user.email  # type: ignore

            # Generate token
            token = TokenGenerator.generate({"user_id": id}, 'email_verification_salt')

            SendEmail({
                'subject': 'For email verification',
                'emails': {
                    'to_emails': email
                },
                'context': {
                    'user': user,
                    'activate_url': f'http://localhost:3000/api/v1/auth/verify-email/{token}/'
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
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])


class EmailVerificationAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('get')

    def post(self, request, *args, **kwargs) -> Response.type:
        token = request.data.get('token', None)

        if token is None:
            return Response.error({
                'message': 'Invalid request',
                'errors': {
                    'token': 'Token can has not be empty'
                }
            }, status.HTTP_400_BAD_REQUEST)

        try:
            data = TokenGenerator.decode(token, 'email_verification_salt')
            user_id = data["user_id"]

            user = User.objects.get(id=user_id)
            if user.is_email_verified:
                return Response.success({
                    'message': 'Email already verified',
                    'data': {
                        'detail': 'Email already verified.'
                    }
                }, status.HTTP_200_OK)

            user.is_email_verified = True
            user.save()
            return Response.success({
                'message': 'Email verified successfully',
                'data': {
                    'detail': 'Email verified successfully'
                }
            }, status.HTTP_200_OK)

        except ValueError as error:
            return Response.error({
                'message': 'Invalid token',
                'errors': {
                    'non_field_errors': [str(error)]
                }
            }, status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        return Response.options(['POST'])


class SigninTokenObtainPairAPIView(TokenObtainPairView):
    """
    Custom JWT token view for user authentication.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = SigninTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle login request and return JWT tokens.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the user from the serializer
        user = serializer.validated_data['user']

        # Enforce email verification for non-superusers
        if not user.is_superuser and not user.is_email_verified:
            return Response.error({
                'message': 'Sign in failed - email not verified',
                'errors': {
                    'non_field_errors': [
                        'Please verify your email address before signing in'
                    ]
                }
            }, status.HTTP_401_UNAUTHORIZED)

        # Update last login timestamp
        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        # Return tokens from the serializer
        return Response.success({
            'message': 'Welcome back! Sign in successful',
            'data': {
                'access_token': serializer.validated_data['access'],
                'refresh_token': serializer.validated_data['refresh'],
            }
        }, status.HTTP_200_OK)


class SigninTokenRefreshAPIView(TokenRefreshView):
    """
    Custom token refresh view for updating JWT tokens.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get_serializer(self, *args, **kwargs) -> TokenRefreshView:
        """
        Customize serializer to handle refresh token field name.
        """
        data = self.request.data.copy()  # type: ignore
        refresh_token = data.pop('refresh_token', None)
        if refresh_token and isinstance(refresh_token, list):
            if len(refresh_token) > 0:
                refresh_token = refresh_token[0]

        if not refresh_token:
            raise serializers.ValidationError({
                'refresh_token': 'This field is required.'
            })

        data['refresh'] = refresh_token
        return super().get_serializer(data=data)

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Handle token refresh requests.
        """
        try:
            print("Before calling super().post")
            response = super().post(request, *args, **kwargs)
            print(f"Response Data: {response.data}")
            if response.status_code == status.HTTP_200_OK:
                return Response.success({
                    'message': 'Access token successfully renewed',
                    'data': {
                        'access_token': response.data.get('access', None)  # type: ignore
                    }
                }, status.HTTP_200_OK)

            # Invalid or expired refresh token
            return Response.error({
                'message': 'Unable to refresh access token',
                'errors': {
                    'non_field_errors': [
                        'Invalid or expired refresh token'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            print(f"Validation Error: {e}")
            # Handle case where no refresh token is provided
            if 'refresh_token' in str(e):
                return Response.error({
                    'message': 'Missing required refresh token',
                    'errors': {
                        'refresh_token': [
                            'This field is required.'
                        ]
                    }
                }, status.HTTP_400_BAD_REQUEST)

            # Catch other validation errors
            return Response.error({
                'message': 'Invalid refresh token',
                'errors': {
                    'refresh_token': [
                        'The refresh token provided is invalid or expired.'
                    ]
                }
            }, status.HTTP_400_BAD_REQUEST)

# class CustomResendVerificationEmailView(APIView):
#     """
#     View for resending account verification emails.

#     Handles requests to resend verification emails for unverified accounts.
#     Validates email existence and verification status before sending.

#     Methods:
#         post: Process email verification resend request

#     Attributes:
#         permission_classes: Allow any user to access
#         throttle_classes: Rate limiting for anonymous requests only
#     """
#     permission_classes = [AllowAny]
#     throttle_classes = [AnonRateThrottle]

#     def post(self, request, *args, **kwargs) -> Response:
#         """
#         Process request to resend verification email.

#         Validates email existence and current verification status
#         before sending new verification email.

#         Args:
#             request: HTTP request containing email address

#         Returns:
#             Response indicating success or error status
#         """
#         email = request.data.get("email", None)

#         if not email:
#             error_context = {
#                 'status': 'failed',
#                 'message': _('Missing email address'),
#                 'error': {
#                     'email': _('Please provide your email address')
#                 }
#             }
#             return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.get(email=email)
#         except User.DoesNotExist:
#             error_context = {
#                 'status': 'failed',
#                 'message': _('Account not found'),
#                 'error': {
#                     'email': _('No account exists with this email address')
#                 }
#             }
#             return Response(error_context, status=status.HTTP_404_NOT_FOUND)

#         if user.emailaddress_set.filter(email=user.email, verified=False).exists():
#             # send_email_confirmation(request, user)
#             success_context = {
#                 'status': 'succeeded',
#                 'message': _('Verification email sent'),
#                 'data': {
#                     'detail': _('Please check your inbox for the verification email')
#                 },
#                 'meta': None
#             }
#             return Response(success_context, status=status.HTTP_200_OK)
#         else:
#             success_context = {
#                 'status': 'succeeded',
#                 'message': _('Email already verified'),
#                 'data': {
#                     'detail': _('Your email address has already been verified')
#                 },
#                 'meta': None
#             }
#             return Response(success_context, status=status.HTTP_400_BAD_REQUEST,)


class UserInfoView(APIView):
    """
    View for retrieving authenticated user information.

    Provides endpoint to get current user's profile data.
    Requires authentication to access.

    Methods:
        get: Retrieve user information

    Attributes:
        permission_classes: Require authentication
        throttle_classes: Rate limiting for authenticated users only
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """
        Retrieve current user's information.

        Serializes and returns authenticated user's profile data.

        Args:
            request: HTTP request from authenticated user

        Returns:
            Response containing serialized user data
        """
        user = request.user
        serializer = UserSerializer(instance=user, many=False)
        return Response.success({
            'message': 'User profile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
