# Local imports
from quick_utils.views import QuickAPIView, Response
from permissions import IsAuthenticated
from throttling import UserRateThrottle
from utils import FieldValidator, SendEmail


class DeactivateAccountView(QuickAPIView):
    """API view for deactivating user accounts."""

    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Deactivate the authenticated user's account."""

        # Get user and password from request
        user = request.user
        password = request.data.get('password', None)

        # Validate the request data
        validator = FieldValidator(request.data, ['password'])
        if not validator.is_valid():
            return self.response({
                "message": "Invalid Password",
                "errors": validator.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        # Verify password matches
        if not user.check_password(password):
            return self.response({
                "message": "Invalid Password",
                "errors": [{
                    "field": "password",
                    "code": "invalid_password",
                    "message": "Your password is not correct.",
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)

        # Deactivate the account
        user.is_active = False
        user.save()

        # Send confirmation email
        SendEmail({
            "subject": "Account Deactivation Confirmation",
            "emails": {
                "to_emails": [user.email]
            },
            "context": {
                "user": user
            },
            "templates": {
                "txt": "users/deactivate_account/confirm_message.txt",
                "html": "users/deactivate_account/confirm_message.html"
            }
        })

        return self.response({
            "message": "Deactivation was successful.",
            "data": {
                "detail": "Your account has been deactivated successfully."
            }
        }, self.status.HTTP_200_OK)
