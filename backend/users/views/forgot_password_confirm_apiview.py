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
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('GET')

    def post(self, request, *args, **kwargs) -> Response.type:
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
            data = TokenGenerator.decode(
                clean_data.get('token'),
                clean_data.get('token_salt')
            )
            user = User.objects.get(id=data["user_id"])
            # Validate the password
            validate_password(clean_data.get('new_password'))
            # Set the new password
            user.set_password(clean_data.get('new_password'))
            user.save()
            return Response.success({
                'message': 'Your password change successfu',
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
        return Response.method_not_allowed('PUT')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('PATCH')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('DELETE')

    def options(self, request, *args, **kwargs) -> Response.type:
        """OPTIONS method not supported."""
        return Response.options(['POST'])