from django.contrib.postgres.forms.hstore import ValidationError
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

# Get the User model configured for the project
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model that handles serialization and deserialization of User objects.

    This serializer provides validation and serialization for the main user fields:
    id, email, first_name, and last_name.

    Fields:
        id (int): Read-only user ID
        email (str): Required. Email address for the user
        first_name (str): Optional. User's first name
        last_name (str): Optional. User's last name

    Validation:
        - ID field is read-only
        - Email is required with custom error messages for required/invalid
        - First name and last name are optional with invalid input error messages

    Note:
        The ID field is marked as read-only both in read_only_fields and extra_kwargs
        for additional security.
    """
    class Meta:
        model = User
        fields = ["id", "email", 'is_email_verified', "first_name", "last_name"]
        read_only_fields = ['id', 'is_email_verified']
        extra_kwargs = {
            'id': {
                'read_only': True
            },
            'is_email_verified': {
                'read_only': True
            },
            'email': {
                'required': True,
                'error_messages': {
                    'required': 'Please provide a valid email address to continue',
                    'invalid': 'The email address format is not valid, please check and try again',
                    'unique': 'This email is already in use. Please provide a different email address.'
                }
            },
            'first_name': {
                'required': False,
                'error_messages': {
                    'invalid': 'The first name contains invalid characters. Please use letters only.'
                }
            },
            'last_name': {
                'required': False,
                'error_messages': {
                    'invalid': 'The last name contains invalid characters. Please use letters only.'
                }
            }
        }

    def create(self, validated_data):
        hashed_password = self.context.get('hashed_password', None)

        if hashed_password is None:
            raise ValidationError('Invalid password')

        # Handle the single record.
        return User.objects.create(password=hashed_password, **validated_data)


class SigninTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer to issue JWT tokens for users, replacing the username
    field with email for authentication.
    """
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        # Authenticate the user
        credentials = {
            'email': attrs['email'],
            'password': attrs['password'],
        }

        user = authenticate(**credentials)
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('This account is inactive')

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        # Include user in the validated data
        return {
            'user': user,
            'access': str(refresh.access_token),  # type: ignore
            'refresh': str(refresh),
        }
