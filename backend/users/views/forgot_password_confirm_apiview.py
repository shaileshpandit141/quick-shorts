# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, TokenGenerator, FieldValidator

User = get_user_model()


class ForgotPasswordConfirmAPIView(APIView):
    """
    API view for confirming and resetting a forgotten password.
    Accepts POST requests with token, token_salt and new password.
    Other HTTP methods are not supported.
    """
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        """GET method not supported."""
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
        """
        Handle POST request to confirm and reset password.

        Args:
            request: HTTP request object containing token, token_salt and new_password

        Returns:
            Response object with success/error message and appropriate status code
        """
        # Validate required fields
        clean_data = FieldValidator(request.data, [
            'token',
            'token_salt',
            'new_password'
        ])
        if not clean_data.is_valid():
            return Response.error({
                'message': 'Invalid request',
                'errors': clean_data.get_errors()
            }, status.HTTP_400_BAD_REQUEST)

        try:
            # Decode token and get user
            data = TokenGenerator.decode(
                clean_data.get('token'),
                clean_data.get('token_salt')
            )
            user = User.objects.get(id=data["user_id"])

            # Validate and set new password
            validate_password(clean_data.get('new_password'))
            user.set_password(clean_data.get('new_password'))
            user.save()

            return Response.success({
                'message': 'Your password change successful',
                'data': {
                    'detail': 'Your password change successfully as for new password'
                }
            }, status.HTTP_200_OK)
        except Exception as error:
            return Response.error({
                'message': 'Invalid request',
                'errors': {
                    'password': error  # type: ignore
                }
            }, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs) -> Response.type:
        """PUT method not supported."""
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        """PATCH method not supported."""
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        """DELETE method not supported."""
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """Return allowed HTTP methods for this endpoint."""
        return Response.options(['POST'])
