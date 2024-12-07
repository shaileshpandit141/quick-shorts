# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated
from throttles import UserRateThrottle
from utils import Response

User = get_user_model()


class ChangePasswordAPIView(APIView):
    """API view for listing and creating YourModel instances.

    Supports GET and POST methods. Other HTTP methods return 400 errors.
    Requires authentication and implements rate limiting.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported."""
        return Response.method_not_allowed('get')

    def post(self, request, *args, **kwargs) -> Response.type:
        """Create one or more new YourModel instances."""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if old_password is None or new_password is None:
            errors = {}
            if old_password is None:
                errors['old_password'] = ['old password can not be empty']
            if new_password is None:
                errors['new_password'] = ['new password can not be empty']

            return Response.error({
                'message': 'Validation error',
                'errors': errors
            }, status.HTTP_400_BAD_REQUEST)

        # Check if the old password is correct
        if not user.check_password(old_password):
            return Response.error({
                'message': 'Old password is incorrect',
                'errors': {
                    'old_password': 'Old password is incorrect'
                }
            }, status.HTTP_400_BAD_REQUEST)

        # Validate the password
        try:
            validate_password(new_password)
        except Exception as error:
            return Response.error({
                'message': 'New password Invalid',
                'errors': {
                    'password': error  # type: ignore
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Set the new password
        user.set_password(new_password)
        user.save()

        return Response.success({
            'message': 'Your password has been changed',
            'data': {
                'detail': 'Your new password has been change successful'
            }
        }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported."""
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported."""
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported."""
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        """OPTIONS method not supported."""
        return Response.options(['POST'])