# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated
from throttles import UserRateThrottle
from utils import Response, FieldValidator, SendEmail


class DeactivateAccountAPIView(APIView):
    """API view for deactivating user accounts.

    Supports POST method for account deactivation.
    Requires authentication and implements rate limiting.
    Other HTTP methods return method not allowed responses.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported for account deactivation."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """Deactivate the authenticated user's account.

        Args:
            request: HTTP request object containing user credentials
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            Response object with success/error message and status code

        Raises:
            None. All errors are handled and returned as Response objects.
        """
        # Get user and password from request
        user = request.user
        password = request.data.get('password', None)

        # Validate the request data
        validator = FieldValidator(request.data, ['password'])
        if not validator.is_valid():
            return Response.error({
                'message': 'Invalid Password',
                'errors': validator.errors
            })

        # Verify password matches
        if not user.check_password(password):
            return Response.error({
                'message': 'Invalid Password',
                'errors': {
                    'password': ['Your password is not correct.']
                }
            })

        # Deactivate the account
        user.is_active = False
        user.save()

        # Send confirmation email
        SendEmail({
            'subject': 'Account Deactivation Confirmation',
            'emails': {
                'to_emails': [user.email]
            },
            'context': {
                'user': user
            },
            'templates': {
                'txt': 'users/deactivate_account/confirm_message.txt',
                'html': 'users/deactivate_account/confirm_message.html'
            }
        })

        return Response.success({
            'message': 'Account deactivation successful',
            'data': {
                'detail': 'Account deactivation successful'
            }
        }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported for account deactivation."""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported for account deactivation."""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported for account deactivation."""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
