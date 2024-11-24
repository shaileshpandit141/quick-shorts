from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """
    Custom user manager that extends Django's BaseUserManager to handle email-based authentication.
    Provides methods for creating regular users and superusers.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.

        Args:
            email: The user's email address
            password: The user's password (optional)
            extra_fields: Additional fields to be saved on the user model

        Returns:
            The created user instance

        Raises:
            ValueError: If email is not provided
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        Sets is_staff, is_superuser and is_active to True by default.

        Args:
            email: The superuser's email address
            password: The superuser's password (optional)
            extra_fields: Additional fields to be saved on the user model

        Returns:
            The created superuser instance

        Raises:
            ValueError: If is_staff or is_superuser is not True
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that uses email as the username field instead of a username.
    Extends Django's AbstractBaseUser and PermissionsMixin.
    """
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)  # Primary identifier for authentication
    first_name = models.CharField(max_length=30, unique=False, blank=True, null=True)  # Optional first name
    last_name = models.CharField(max_length=30, unique=False, blank=True, null=True)  # Optional last name
    date_joined = models.DateTimeField(auto_now_add=True, blank=False, null=False)  # Automatically set when account is created
    last_login = models.DateTimeField(auto_now=True, blank=False, null=False)  # Automatically updated on each login
    is_active = models.BooleanField(default=False)  # Whether this user should be treated as active
    is_staff = models.BooleanField(default=False)  # Whether this user can access the admin site
    is_superuser = models.BooleanField(default=False)  # Whether this user has all permissions without explicitly assigning them

    objects = UserManager()

    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # Email & password are required by default

    class Meta:
        db_table = 'users'  # Custom database table name
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']  # Order users by join date (newest first)
        unique_together = (('email', 'first_name'), ('email', 'last_name'), ('first_name', 'last_name'))  # Enforce unique combinations

    def __str__(self):
        """Returns the string representation of the user (email)"""
        return self.email

    def get_full_name(self):
        """Returns the user's full name, with a space between first and last name"""
        return f'{self.first_name} {self.last_name}'.strip()
