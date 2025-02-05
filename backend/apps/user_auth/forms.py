from django import forms
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.validators import validate_email

from .models import User


class UserCreationForm(DjangoUserCreationForm):
    """A form for creating new users. Extends Django's built-in UserCreationForm."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Your password must contain at least 8 characters.",
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Enter the same password as above, for verification.",
    )
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control"}), required=False
    )
    avatar = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "form-control"}), required=False
    )
    is_active = forms.BooleanField(required=False)
    is_verified = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_active",
            "is_verified",
            "is_staff",
        )

    def clean_email(self):
        """Custom validation for email field."""

        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")

        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")

        if User.objects.filter(email=email.lower()).exists():
            raise forms.ValidationError("A user with this email already exists.")

        return email.lower()

    def clean_password2(self):
        """Verify that both passwords match and meet minimum requirements."""

        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

        if password1 is None:
            raise forms.ValidationError("Password is required")

        if len(str(password1)) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long")

        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(DjangoUserChangeForm):
    """A form for updating users. Extends Django's built-in UserChangeForm."""

    email = forms.EmailField(
        required=True, widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        required=True, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    first_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        required=False, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(
            attrs={"class": "form-control", "style": "margin-block: 8px;"}
        ),
    )
    is_active = forms.BooleanField(required=False)
    is_verified = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)

    class Meta(DjangoUserChangeForm.Meta):
        model = User
        fields = (
            "email",
            "username",
            "first_name",
            "last_name",
            "avatar",
            "is_active",
            "is_verified",
            "is_staff",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.avatar:
            self.fields[
                "avatar"
            ].help_text = f'<a href="{self.instance.avatar.url}" target="_blank" style="padding-inline: 4px;">View Current Avatar</a>'

    def clean_email(self):
        """Validation for email field."""

        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Email is required.")

        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError("Please enter a valid email address.")

        return email.lower()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
