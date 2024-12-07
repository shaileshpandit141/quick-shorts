# Django imports
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

# Django REST framework imports
from rest_framework import status
from rest_framework.views import APIView

# Local imports
from permissions import AllowAny
from throttles import AnonRateThrottle
from utils import Response, TokenGenerator

User = get_user_model()


class ForgotPasswordConfirmAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    def get(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('get')

    def post(self, request, *args, **kwargs) -> Response.type:
        token = request.data.get('token', None)
        token_salt = request.data.get('token_salt', None)
        new_password = request.data.get('new_password', None)

        if token is None or token_salt is None or new_password is None:
            errors = {}
            if token is None:
                errors['token'] = ['Token `token` can has not be empty']
            if token_salt is None:
                errors['token_salt'] = ['Token salt `token_salt` can has not be empty']
            if new_password is None:
                errors['new_password'] = ['New password `new_password` can has not be empty']

            return Response.error({
                'message': 'Invalid request',
                'errors': errors
            }, status.HTTP_400_BAD_REQUEST)

        try:
            data = TokenGenerator.decode(token, token_salt)
            user_id = data["user_id"]
            user = User.objects.get(id=user_id)

            # Validate the password
            validate_password(new_password)
            # Set the new password
            user.set_password(new_password)
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
        return Response.method_not_allowed('put')

    def patch(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('patch')

    def delete(self, request, *args, **kwargs) -> Response.type:
        return Response.method_not_allowed('delete')

    def options(self, request, *args, **kwargs) -> Response.type:
        """OPTIONS method not supported."""
        return Response.options(['POST'])