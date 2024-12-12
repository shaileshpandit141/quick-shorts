from typing import TypedDict, Dict, List, NotRequired
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
import logging

# Set up a logger
logger = logging.getLogger(__name__)

class EmailsType(TypedDict):
    from_email: NotRequired[str]
    to_emails: List[str]


class TemplatesType(TypedDict):
    txt: str
    html: str


class EmailCredentialType(TypedDict):
    subject: str
    emails: EmailsType
    context: Dict
    templates: TemplatesType


class SendEmail:
    def __init__(self, emailCredential: EmailCredentialType) -> None:
        self.subject = emailCredential['subject']
        self.from_email = emailCredential['emails'].get(
            'from_email',
            settings.DEFAULT_FROM_EMAIL
        )

        if not isinstance(emailCredential['emails']['to_emails'], list):
            raise Exception("Invalid to_email data type")

        self.to_emails = emailCredential['emails']['to_emails']
        self.context = emailCredential['context']
        self.text_template = emailCredential['templates']['txt']
        self.html_template = emailCredential['templates']['html']

        self.successful_email_send = []
        self.fallback_successful_email_send = []

        self._validate_templates()
        self.unique_to_emails = self._get_unique_to_emails()

        self._send_email()

    def _is_valid_email(self, email: str) -> bool:
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False

    def _get_unique_to_emails(self) -> List[str]:
        processed_email_list = []
        for email in self.to_emails:
            if not self._is_valid_email(email):
                email = self.from_email
            if email not in processed_email_list:
                processed_email_list.append(email)
        return processed_email_list

    def _validate_templates(self) -> None:
        if not self.text_template.endswith(".txt"):
            raise ValidationError("Text template must be a .txt file")
        if not self.html_template.endswith(".html"):
            raise ValidationError("HTML template must be a .html file")

    def _send_email(self) -> None:
        try:
            # Render email templates
            text_content = render_to_string(self.text_template, self.context)
            html_content = render_to_string(self.html_template, self.context)

            # Create and send the email
            email = EmailMultiAlternatives(
                self.subject,
                text_content,
                self.from_email,
                self.unique_to_emails
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

            # Track the successful email send
            self.successful_email_send = self.unique_to_emails
            logger.info(f"Email sent successfully to: {', '.join(self.unique_to_emails)}")

        except Exception as e:
            logger.error(f"Error sending email to {self.unique_to_emails}: {e}")
            # Fallback to sending to from_email
            self._send_fallback_email()

    def _send_fallback_email(self) -> None:
        try:
            text_content = render_to_string(self.text_template, self.context)
            html_content = render_to_string(self.html_template, self.context)

            fallback_email = EmailMultiAlternatives(
                self.subject,
                text_content,
                self.from_email,
                [self.from_email]
            )
            fallback_email.attach_alternative(html_content, "text/html")
            fallback_email.send()

            # Track the fallback successful send
            self.fallback_successful_email_send = [self.from_email]
            logger.info(f"Fallback email sent to: {self.from_email}")

        except Exception as e:
            logger.error(f"Error sending fallback email: {e}")
