# Django imports
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Django REST framework imports
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

# REST framework SimpleJWT imports
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Django REST Auth imports
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LogoutView, PasswordResetConfirmView, PasswordResetView

# All Auth imports
from allauth.account.utils import send_email_confirmation

# Local imports
from .serializers import UserSerializer, CustomTokenObtainPairSerializer


User = get_user_model()


class CustomRegisterView(RegisterView):
    """
    Custom registration view for creating new user accounts.

    Extends the default RegisterView to provide custom response formatting
    and token generation on successful registration.

    Attributes:
        permission_classes: Allow any user to access this endpoint
        throttle_classes: Rate limiting for anonymous requests
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def create(self, request, *args, **kwargs):
        """
        Handle user registration requests.

        Validates registration data and creates new user account.
        Generates JWT tokens upon successful registration.

        Args:
            request: HTTP request containing registration data

        Returns:
            Response with JWT tokens or validation errors
        """
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = self.perform_create(serializer)
            refresh = self.get_token(user)  # type: ignore

            success_context = {
                'status': 'success',
                'message': _('Registration successful! Welcome aboard!'),
                'data': {
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh)
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_201_CREATED)

        error_context = {
            'status': 'error',
            'message': _('Registration failed. Please check your information.'),
            'error': serializer.errors
        }
        return Response(error_context, status=status.HTTP_400_BAD_REQUEST)


class CustomLogoutView(LogoutView):
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
                'status': 'error',
                'message': _('Sign out failed - refresh token required'),
                'error': {
                    'refresh_token': _('Please provide your refresh token')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            error_context = {
                'status': 'error',
                'message': _('Sign out failed - invalid token'),
                'error': {
                    'refresh_token': _('The provided refresh token is not valid')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        super().post(request, *args, **kwargs)

        success_context = {
            'status': 'success',
            'message': _('Goodbye! You have been successfully logged out'),
            'data': {
                'detail': _('Sign out completed successfully')
            },
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)


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
                'status': 'error',
                'message': _('Sign in failed - invalid credentials'),
                'error': serializer.errors
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.user

        if not user.is_superuser:
            if not user.emailaddress_set.filter(verified=True).exists():
                error_context = {
                    'status': 'error',
                    'message': _('Sign in failed - email not verified'),
                    'error': _('Please verify your email address before logging in')
                }
                return Response(error_context, status=status.HTTP_401_UNAUTHORIZED)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        refresh = RefreshToken.for_user(user)

        success_context = {
            'status': 'success',
            'message': _('Welcome back! Sign in successful'),
            'data': {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            },
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom token refresh view for updating JWT tokens.

    Extends TokenRefreshView to handle refresh token updates with custom
    request/response formatting.

    Attributes:
        permission_classes: Allow any user to access
        throttle_classes: Rate limiting for anonymous requests
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get_serializer(self, *args, **kwargs):
        """
        Customize serializer to handle refresh token field name.

        Modifies request data to use 'refresh_token' instead of 'refresh'.

        Returns:
            Serializer instance with modified data
        """
        data = self.request.data
        try:
            data['refresh'] = data.pop('refresh_token')  # type: ignore
        except KeyError:
            pass
        return super().get_serializer(data=data, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle token refresh requests.

        Process refresh token and return new access token.

        Args:
            request: HTTP request with refresh token

        Returns:
            Response with new access token or error details
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            success_context = {
                'status': 'success',
                'message': _('Access token successfully renewed'),
                'data': {
                    'access_token': response.data.get('access')  # type: ignore
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_200_OK)

        error_context = {
            'status': _('error'),
            'message': _('Unable to refresh access token'),
            'error': response.data
        }
        return Response(error_context, status=response.status_code)


class CustomVerifyEmailView(VerifyEmailView):
    """
    Custom view for verifying user email addresses.

    Extends VerifyEmailView to provide custom response formatting
    for email verification results.

    Attributes:
        permission_classes: Allow any user to access
        throttle_classes: Rate limiting for anonymous requests
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        """
        Process email verification request.

        Verifies email token and updates user verification status.

        Args:
            request: HTTP request with verification token

        Returns:
            Response indicating verification success or failure
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            success_context = {
                'status': 'success',
                'message': _('Great! Your email has been verified'),
                'data': {
                    'detail': _('Email verification completed successfully')
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_200_OK)

        error_context = {
            'status': 'error',
            'message': _('Unable to verify email address'),
            'error': response.data
        }
        return Response(error_context, status=response.status_code)


class CustomResendVerificationEmailView(APIView):
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
                'status': 'error',
                'message': _('Missing email address'),
                'error': {
                    'email': _('Please provide your email address')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            error_context = {
                'status': 'error',
                'message': _('Account not found'),
                'error': {
                    'email': _('No account exists with this email address')
                }
            }
            return Response(error_context, status=status.HTTP_404_NOT_FOUND)

        if user.emailaddress_set.filter(email=user.email, verified=False).exists():
            send_email_confirmation(request, user)
            success_context = {
                'status': 'success',
                'message': _('Verification email sent'),
                'data': {
                    'detail': _('Please check your inbox for the verification email')
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_200_OK)
        else:
            success_context = {
                'status': 'success',
                'message': _('Email already verified'),
                'data': {
                    'detail': _('Your email address has already been verified')
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
                'status': 'error',
                'message': _('Missing email address'),
                'error': {
                    'email': _('Please provide your email address')
                }
            }
            return Response(error_context, status=status.HTTP_400_BAD_REQUEST)

        if not User.objects.filter(email=email).exists():
            error_context = {
                'status': 'error',
                'message': _('Account not found'),
                'error': {
                    'email': _('No account exists with this email address')
                }
            }
            return Response(error_context, status=status.HTTP_404_NOT_FOUND)

        return super().post(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """
    Custom view for confirming password reset requests.

    Extends PasswordResetConfirmView to provide custom response formatting
    for password reset confirmation results.

    Attributes:
        permission_classes: Allow any user to access
        throttle_classes: Rate limiting for anonymous requests
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        """
        Process password reset confirmation request.

        Validates reset token and updates user password.

        Args:
            request: HTTP request with reset token and new password

        Returns:
            Response indicating reset success or failure
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            success_context = {
                'status': 'success',
                'message': _('Password successfully updated'),
                'data': {
                    'detail': _('You can now sign in with your new password')
                },
                'meta': None
            }
            return Response(success_context, status=status.HTTP_200_OK)

        error_context = {
            'status': 'error',
            'message': _('Unable to reset password'),
            'error': response.data
        }
        return Response(error_context, status=response.status_code)


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
            'status': 'success',
            'message': _('User profile retrieved successfully'),
            'data': serializer.data,
            'meta': None
        }
        return Response(success_context, status=status.HTTP_200_OK)
