# Django imports
from django.contrib.auth import get_user_model

# Local imports
from quick_utils.views import QuickAPIView, Response
from permissions import AllowAny
from throttling import AuthRateThrottle
from utils import TokenGenerator, FieldValidator

User = get_user_model()


class VerifyAccountConfirmView(QuickAPIView):
    """API View for verifying user accounts via email confirmation."""

    permission_classes = [AllowAny]
    throttle_classes = [AuthRateThrottle]

    def post(self, request, *args, **kwargs) -> Response:
        """Handle POST request for email verification"""

        # Validate required fields
        clean_data = FieldValidator(request.data, ['token', 'token_salt'])
        if not clean_data.is_valid:
            return self.response({
                'message': 'Invalid request',
                'errors': clean_data.errors
            }, self.status.HTTP_400_BAD_REQUEST)

        try:
            # Decode verification token
            data = TokenGenerator.decode(
                clean_data.get('token'),
                clean_data.get('token_salt')
            )
            user = User.objects.get(id=data["user_id"])

            # Check if already verified
            if user.is_verified:
                return self.response({
                    'message': 'Account already verified',
                    'data': {
                        'detail': 'Account already verified.'
                    }
                }, self.status.HTTP_200_OK)

            # Update verification status
            user.is_verified = True
            user.save()
            return self.response({
                'message': 'Account verified successfully',
                'data': {
                    'detail': 'Account verified successfully'
                }
            }, self.status.HTTP_200_OK)

        except ValueError as error:
            return self.response({
                'message': 'Invalid token',
                'errors': [{
                    "field": "token",
                    "code": "invalid",
                    "message": str(error),
                    "details": None
                }]
            }, self.status.HTTP_400_BAD_REQUEST)
