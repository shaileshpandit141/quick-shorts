# Django imports
from django.contrib.auth import get_user_model
from django.contrib.postgres.forms.hstore import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Django REST framework imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

# REST framework SimpleJWT imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password

# Local imports
from utils.response import Response
from utils.send_email import SendEmail
from utils.token_generator import TokenGenerator
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


User = get_user_model()


class UserRegisterAPIView(APIView):
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
        except ValidationError as e:
            return Response.error({
                'message': 'Invalid password',
                'errors': {
                    'password': [str(msg) for msg in list(e.messages)]
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
            token = TokenGenerator.generate({"id": id}, 'email_verification_salt')

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


# class CustomTokenObtainPairView(TokenObtainPairView):
#     """
#     Custom JWT token view for user authentication.

#     Extends TokenObtainPairView to provide JWT tokens for authentication. Validates user
#     credentials and enforces email verification requirements before issuing tokens.

#     Methods:
#         post: Handle login requests and return JWT tokens

#     Attributes:
#         permission_classes: Allow any user to access this endpoint
#         throttle_classes: Rate limiting for anonymous requests only
#         serializer_class: Custom serializer for token generation
#     """
#     permission_classes = [AllowAny]
#     throttle_classes = [AnonRateThrottle]
#     serializer_class = CustomTokenObtainPairSerializer

#     def post(self, request, *args, **kwargs) -> Response:
#         """
#         Handle login request and generate JWT tokens.

#         Validates user credentials, checks email verification status for non-superusers,
#         updates last login timestamp, and returns access and refresh tokens.

#         Args:
#             request: HTTP request object containing login credentials

#         Returns:
#             Response with JWT tokens or error details
#         """
#         serializer = self.get_serializer(data=request.data, many=False)

#         if not serializer.is_valid():
#             error_context = {
#                 'status': 'failed',
#                 'message': _('Sign in failed - invalid credentials'),
#                 'error': serializer.errors
#             }
#             return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

#         user = serializer.user

#         if not user.is_superuser:
#             if not user.emailaddress_set.filter(verified=True).exists():
#                 error_context = {
#                     'status': 'failed',
#                     'message': _('Sign in failed - email not verified'),
#                     'error': {
#                         'non_field_errors': [
#                             _('Please verify your email address before logging in')
#                         ]
#                     }
#                 }
#                 return Response(error_context, status=status.HTTP_401_UNAUTHORIZED)

#         user.last_login = timezone.now()
#         user.save(update_fields=["last_login"])

#         refresh = RefreshToken.for_user(user)

#         success_context = {
#             'status': 'succeeded',
#             'message': _('Welcome back! Sign in successful'),
#             'data': {
#                 'access_token': str(refresh.access_token),
#                 'refresh_token': str(refresh)
#             },
#             'meta': None
#         }
#         return Response(success_context, status=status.HTTP_200_OK)


# class CustomTokenRefreshView(TokenRefreshView):
#     """
#     Custom token refresh view for updating JWT tokens.

#     Extends TokenRefreshView to handle refresh token updates with custom
#     request/response formatting.

#     Attributes:
#         permission_classes: Allow any user to access
#         throttle_classes: Rate limiting for anonymous requests
#     """
#     permission_classes = [AllowAny]
#     throttle_classes = [AnonRateThrottle]

#     def get_serializer(self, *args, **kwargs) -> NoReturn:
#         """
#         Customize serializer to handle refresh token field name.

#         Modifies request data to use 'refresh_token' instead of 'refresh'.

#         Returns:
#             Serializer instance with modified data
#         """
#         data = self.request.data
#         try:
#             data['refresh'] = data.pop('refresh_token')  # type: ignore
#         except KeyError:
#             pass
#         return super().get_serializer(data=data, *args, **kwargs)

#     def post(self, request, *args, **kwargs) -> Response:
#         """
#         Handle token refresh requests.

#         Process refresh token and return new access token.

#         Args:
#             request: HTTP request with refresh token

#         Returns:
#             Response with new access token or error details
#         """
#         response = super().post(request, *args, **kwargs)

#         if response.status_code == status.HTTP_200_OK:
#             success_context = {
#                 'status': 'succeeded',
#                 'message': _('Access token successfully renewed'),
#                 'data': {
#                     'access_token': response.data.get('access')  # type: ignore
#                 },
#                 'meta': None
#             }
#             return Response(success_context, status=status.HTTP_200_OK)

#         error_context = {
#             'status': _('error'),
#             'message': _('Unable to refresh access token'),
#             'error': response.data
#         }
#         return Response(error_context, status=response.status_code)


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
