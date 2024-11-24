from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from allauth.account.utils import send_email_confirmation
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from dj_rest_auth.views import PasswordResetView, LogoutView


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view for user authentication.

    Extends TokenObtainPairView to provide JWT tokens for authentication. Validates user
    credentials and enforces email verification requirements before issuing tokens.

    Methods:
        post: Handle login requests and return JWT tokens

    Attributes:
        permission_classes: Allow any user to access this endpoint
        throttle_classes: Rate limiting for anonymous requests only
        serializer_class: Custom serializer for token generation
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        Handle login request and generate JWT tokens.

        Validates user credentials, checks email verification status for non-superusers,
        updates last login timestamp, and returns access and refresh tokens.

        Args:
            request: HTTP request object containing login credentials

        Returns:
            Response with JWT tokens or error details
        """
        serializer = self.get_serializer(data=request.data, many=False)

        if not serializer.is_valid():
            error_context = {
                'status': _('error'),
                'message': _('The request was not successful'),
                'error': serializer.errors
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.user

        if not user.is_superuser:
            if not user.emailaddress_set.filter(verified=True).exists():
                error_context = {
                    'status': _('error'),
                    'message': _('The request was not successful'),
                    'error': _('The email address is not verified.')
                }
                return Response(error_context ,status=status.HTTP_401_UNAUTHORIZED)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        refresh = RefreshToken.for_user(user)

        success_context = {
            'status': _('success'),
            'message': _('The request was successful'),
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            },
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)


class CustomSignoutView(LogoutView):
    """
    Custom view for handling user logout.

    Extends LogoutView to handle JWT token blacklisting and session cleanup.
    Requires authentication and validates refresh token before logout.

    Methods:
        post: Handle logout request and blacklist refresh token

    Attributes:
        permission_classes: Require authentication
        throttle_classes: Rate limiting for authenticated users only
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs):
        """
        Handle logout request and invalidate refresh token.

        Checks for refresh token presence, blacklists it if valid,
        and cleans up user session.

        Args:
            request: HTTP request containing refresh token

        Returns:
            Response indicating logout success or error
        """
        refresh_token = request.data.get("refresh_token", None)

        if refresh_token is None:
            error_context = {
                'status': _('error'),
                'message': _('The request was not successful'),
                'error': {
                    'refresh_token': _('This field cannot be blank.')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            error_context = {
                'status': _('error'),
                'message': _('Invalid refresh token'),
                'error': {
                    'refresh_token': _('Invalid refresh token')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        super().post(request, *args, **kwargs)

        success_context = {
            'status': _('success'),
            'message': _('The request was successful'),
            'data': {
                'detail': _('You have signed out successfully.')
            },
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)


class ResendVerificationEmailView(APIView):
    """
    View for resending account verification emails.

    Handles requests to resend verification emails for unverified accounts.
    Validates email existence and verification status before sending.

    Methods:
        post: Process email verification resend request

    Attributes:
        permission_classes: Allow any user to access
        throttle_classes: Rate limiting for anonymous requests only
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request):
        """
        Process request to resend verification email.

        Validates email existence and current verification status
        before sending new verification email.

        Args:
            request: HTTP request containing email address

        Returns:
            Response indicating success or error status
        """
        email = request.data.get("email", None)

        if not email:
            error_context = {
                'status': _('error'),
                'message': _('This email field cannot be blank.'),
                'error': {
                    'email': _('This field cannot be blank.')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_context = {
                'status': _('error'),
                'message': _('User does not exist'),
                'error': {
                    'username': _('User with this email does not exist.')
                }
            }
            return Response(error_context, status=status.HTTP_404_NOT_FOUND)

        if user.emailaddress_set.filter(email=user.email, verified=False).exists():
            send_email_confirmation(request, user)
            success_context = {
                'status': _('success'),
                'message': _('The request was successful'),
                'data': {
                    'detail': _('The email verification e-mail has been sent.')
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_200_OK)
        else:
            success_context = {
                'status': _('success'),
                'message': _('The request was successful'),
                'data': {
                    'detail': _('This email is already verified.')
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_400_BAD_REQUEST,)


class CustomPasswordResetView(PasswordResetView):
    """
    Custom view for handling password reset requests.

    Extends PasswordResetView to add additional validation and custom responses.
    Handles email validation and initiates password reset process.

    Methods:
        post: Handle password reset request

    Attributes:
        permission_classes: Allow any user to access
        throttle_classes: Rate limiting for anonymous requests only
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        """
        Process password reset request.

        Validates email existence before initiating password reset.

        Args:
            request: HTTP request containing email address

        Returns:
            Response indicating success or error status
        """
        email = request.data.get("email", None)
        if not email:
            error_context = {
                'status': _('error'),
                'message': _('Invalid email address'),
                'error': {
                    'email': _('This email field cannot be blank.')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            error_context = {
                'status': _('error'),
                'message': _('Email does not exist'),
                'error': {
                    'email': _('This email address does not exist.')
                }
            }
            return Response(error_context, status=status.HTTP_404_NOT_FOUND)

        return super().post(request, *args, **kwargs)


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

    def get(self, request):
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
        success_context = {
            'status': _('success'),
            'message': _('The request was successful'),
            'data': serializer.data,
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)


class ProtectedView(APIView):
    """
    Protected test endpoint requiring authentication.

    Simple view for testing authentication and authorization.
    Returns success message for authenticated requests.

    Methods:
        get: Test protected access

    Attributes:
        permission_classes: Require authentication
        throttle_classes: Rate limiting for authenticated users only
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        """
        Test protected endpoint access.

        Returns success message if user is authenticated.

        Args:
            request: HTTP request from authenticated user

        Returns:
            Response confirming protected access
        """
        success_context = {
            'status': _('success'),
            'message': _('The request was successful'),
            'data': {
                'detail': _('This is a protected route.')
            },
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)
