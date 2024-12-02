from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from decouple import config


class UserAdapter(DefaultAccountAdapter):
    """Custom adapter for Django-allauth that handles email operations.

    This adapter extends Django-allauth's DefaultAccountAdapter to provide custom email
    functionality for user account verification and password reset workflows. It uses
    customizable email templates and configurable frontend URLs.

    The adapter reads host and port configuration from environment variables to construct
    verification/reset URLs that point to the frontend application.

    Environment Variables:
        SEND_VERIFICATION_URL_HOST: Host for verification URLs (default: localhost)
        SEND_VERIFICATION_URL_PORT: Port for verification URLs (default: 3000)
    """

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        """Send a customized email verification mail to users.

        This method constructs and sends an HTML/text email to verify a user's email address.
        The verification link points to a frontend route that can handle the verification.

        Args:
            request: Django HttpRequest object for the current request
            emailconfirmation: EmailConfirmation instance containing the verification key
                and email address details
            signup: Boolean flag indicating if this is for a new user signup (unused)

        Note:
            The verification URL is constructed using configured HOST and PORT values,
            with format: http://{host}:{port}/verify-account/{verification_key}/
        """
        # Read host/port config with defaults
        HOST = config("SEND_VERIFICATION_URL_HOST", cast=str, default="localhost")
        PORT = config("SEND_VERIFICATION_URL_PORT", cast=str, default="3000")

        # Build verification URL and context
        activate_url = f"http://{HOST}:{PORT}/verify-account/{emailconfirmation.key}/"

        context = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": request.get_host(),
            "key": emailconfirmation.key,
        }

        # Template paths for email content
        email_template_txt = "user_account/email/email_confirmation_message.txt"
        email_template_html = "user_account/email/email_confirmation_message.html"

        # Render email content from templates
        subject = "Confirm your email address"
        message_txt = render_to_string(email_template_txt, context)
        message_html = render_to_string(email_template_html, context)

        # Construct and send multi-part email
        email = EmailMultiAlternatives(
            subject,
            message_txt,
            settings.DEFAULT_FROM_EMAIL,
            [emailconfirmation.email_address.email],
        )

        email.attach_alternative(message_html, "text/html")
        email.send(fail_silently=False)

    def send_mail(self, template_prefix, email, context):
        """Send a customized password reset email to users.

        This method constructs and sends an HTML/text email containing password reset instructions.
        The reset link points to a frontend route that can handle the password reset flow.

        Args:
            template_prefix: Base template name prefix (unused in this implementation)
            email: Recipient email address string
            context: Dictionary containing reset details including:
                - uid: User ID encoded for the reset URL
                - token: Reset token for verification

        Note:
            The reset URL is constructed using configured HOST and PORT values,
            with format: http://{host}:{port}/password-reset-confirm/{uid}/{token}/
        """
        # Only proceed with URL construction if we have necessary context
        if "uid" in context and "token" in context:
            HOST = config("SEND_VERIFICATION_URL_HOST", cast=str, default="localhost")
            PORT = config("SEND_VERIFICATION_URL_PORT", cast=str, default="3000")

            password_reset_url = f"http://{HOST}:{PORT}/password-reset-confirm/{context['uid']}/{context['token']}/"
            context["password_reset_url"] = password_reset_url

        # Template paths for email content
        email_template_txt = "user_account/email/password_reset_key_message.txt"
        email_template_html = "user_account/email/password_reset_key_message.html"

        # Render email content from templates
        message_txt = render_to_string(email_template_txt, context)
        message_html = render_to_string(email_template_html, context)

        # Construct and send multi-part email
        subject = "Reset Your Password"
        email_message = EmailMultiAlternatives(
            subject,
            message_txt,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )

        email_message.attach_alternative(message_html, "text/html")
        email_message.send(fail_silently=False)

    def populate_username(self, request, user):
        # Do nothing as we're using email as the identifier
        pass
