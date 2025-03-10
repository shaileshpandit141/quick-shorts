from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.forms.hstore import ValidationError
from rest_framework import serializers

# Get the User model configured for the project
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model that handles serialization and deserialization of User objects."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_verified",
            "is_staff",
            "is_superuser",
        ]
        read_only_fields = ["id", "usename", "is_verified", "is_staff", "is_superuser"]

    def create(self, validated_data) -> AbstractUser:
        hashed_password = self.context.get("hashed_password", None)

        email = validated_data.get("email")
        username = email.split("@")[0]

        if hashed_password is None:
            raise ValidationError("Invalid password")

        # Handle the single record.
        return User.objects.create(
            password=hashed_password, username=username, **validated_data
        )


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for User model that handles serialization and deserialization of User objects."""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "avatar"]
