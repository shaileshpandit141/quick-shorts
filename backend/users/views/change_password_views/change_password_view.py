# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Local imports
from quick_utils.views import APIView, Response
from permissions import IsAuthenticated
from throttling import AuthRateThrottle
from utils import FieldValidator
from quick_utils.send_email import SendEmail


User = get_user_model()


class ChangePasswordView(APIView):
    """Changes authenticated user's password."""
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Changes user password after validation."""

        user = request.user

        # Validate required fields
        clean_data = FieldValidator(request.data, [
            "old_password",
            "new_password"
        ])

        if not clean_data.is_valid():
            return self.response({
                "message": "Please provide both old and new passwords",
                "errors": clean_data.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        # Check if old password is correct
        if not user.check_password(clean_data.get('old_password')):
            return self.response({
                "message": "The old password you entered is incorrect",
                "errors": [{
                    "field": "old_password",
                    "code": "old_password_incorrect",
                    "message": "Please enter your current password correctly",
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        # Validate new password complexity
        try:
            validate_password(clean_data.get('new_password'))
        except Exception as error:
            return self.response({
                "message": "Your new password does not meet the requirements",
                "errors": [{
                    "field": "new_password",
                    "code": "invalid_password",
                    "message": str(error),
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        # Set new password and notify user via email
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
        return self.response({
            'message': 'Password updated successfully',
            'data': {
                'detail': 'Your password has been changed. Please use your new password for future signin.'
            }
        }, self.status.HTTP_200_OK)
