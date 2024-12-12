# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import IsAuthenticated
from throttles import UserRateThrottle
from utils import Response, SendEmail, FieldValidator

User = get_user_model()


class ChangePasswordAPIView(APIView):
    """API view for changing user password.

    Supports only POST method for changing password.
    Requires authentication and implements rate limiting.
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported for password change."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """Change user password.

        Args:
            request: HTTP request containing old_password and new_password

        Returns:
            Response with success/error message

        Raises:
            400 Bad Request: If validation fails or old password is incorrect
        """
        user = request.user

        # Validate required fields
        clean_data = FieldValidator(request.data, [
            'old_password',
            'new_password'
        ])

        if not clean_data.is_valid():
            return Response.error({
                'message': 'Validation error',
                'errors': clean_data.get_errors()
            }, status.HTTP_400_BAD_REQUEST)

        # Verify current password is correct
        if not user.check_password(clean_data.get('old_password')):
            return Response.error({
                'message': 'Old password is incorrect',
                'errors': {
                    'old_password': 'Old password is incorrect'
                }
            }, status.HTTP_400_BAD_REQUEST)

        # Validate new password meets requirements
        try:
            validate_password(clean_data.get('new_password'))
        except Exception as error:
            return Response.error({
                'message': 'New password Invalid',
                'errors': {
                    'password': error  # type: ignore
                }
            }, status=status.HTTP_400_BAD_REQUEST)

        # Update password and notify user
        user.set_password(clean_data.get('new_password'))
        user.save()
        SendEmail({
            'subject': 'Password Change Notification',
            'emails': {
                'to_emails': [user.email]
            },
            'context': {
                'user': user
            },
            'templates': {
                'txt': 'users/change_password/success_message.txt',
                'html': 'users/change_password/success_message.html'
            }
        })
        return Response.success({
            'message': 'Your password has been changed',
            'data': {
                'detail': 'Your new password has been changed successfully'
            }
        }, status.HTTP_200_OK)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported for password change."""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported for password change."""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported for password change."""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
