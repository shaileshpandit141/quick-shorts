from typing import Dict, List, NotRequired, TypedDict


class EmailsType(TypedDict):
    """Type definition for email addresses in the email system.

    Attributes:
        from_email: Optional sender email address
        to_emails: List of recipient email addresses
    """

    from_email: NotRequired[str]
    to_emails: List[str]


class TemplatesType(TypedDict):
    """Type definition for email templates.

    Attributes:
        txt: Plain text version of the email template
        html: HTML version of the email template
    """

    txt: str
    html: str


class EmailCredentialType(TypedDict):
    """Type definition for complete email configuration.

    Attributes:
        subject: Email subject line
        emails: Email addresses configuration
        context: Dictionary containing template variables
        templates: Email template configurations
    """

    subject: str
    emails: EmailsType
    context: Dict
    templates: TemplatesType
