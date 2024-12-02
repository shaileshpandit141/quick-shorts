from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm


class UserCreationForm(DjangoUserCreationForm):
    """
    A form for creating new users. Extends Django's built-in UserCreationForm.

    Includes fields for email, first name, last name, active status, and staff status.
    Adds custom validation for unique email addresses.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_email_verified')

    def clean_email(self):
        """
        Custom validation for email field.

        Returns:
            str: The validated email address

        Raises:
            ValidationError: If a user with this email already exists
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email


class UserChangeForm(DjangoUserChangeForm):
    """
    A form for updating users. Extends Django's built-in UserChangeForm.

    Includes fields for email, first name, last name, active status, and staff status.
    Adds validation to ensure email is provided.
    """
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_email_verified')

    def clean_email(self):
        """
        Validation for email field.

        Returns:
            str: The validated email address

        Raises:
            ValidationError: If email field is empty
        """
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("This field is required.")
        return email
