from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .forms import UserCreationForm, UserChangeForm

class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for User model that extends Django's built-in UserAdmin.
    Customizes the admin forms, display fields and fieldsets for managing users.
    """
    model = User
    add_form = UserCreationForm  # Custom form for creating new users
    form = UserChangeForm  # Custom form for modifying existing users

    # Fields to display in the user list view
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_email_verified')
    search_fields = ('email',)  # Enable searching by email
    readonly_fields = ('date_joined', 'last_login')  # Fields that cannot be modified

    # Define how fields are grouped and displayed when editing existing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_email_verified')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Define fields shown when adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active', 'is_email_verified')
        }),
    )

    ordering = ('email',)  # Default ordering by email address

# Register the custom admin interface
admin.site.register(User, CustomUserAdmin)
