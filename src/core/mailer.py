"""
Module for send mail.
"""
import sys
import traceback
from django.core import mail

from django.core.mail import send_mail, EmailMessage
from django.template.loader import get_template


class TemplateEmailMessage(EmailMessage):
    """A container for email information."""

    def __init__(# pylint: disable=R0913
        self,
        template,
        context_data,
        subject="",
        from_email=None,
        to=None,
        bcc=None,
        connection=None,
        attachments=None,
        headers=None,
        cc=None,
        reply_to=None,
    ):
        """
        Initialize a single email message (which can be sent to multiple
        recipients).
        """
        template = get_template(template)
        body = template.render(context_data)
        super().__init__(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to,
            bcc=bcc,
            connection=connection,
            attachments=attachments,
            headers=headers,
            cc=cc,
            reply_to=reply_to,
        )


def send_template_mail( # pylint: disable=R0913
    template,
    context_data,
    subject,
    recipient_list,
    from_email=None,
    fail_silently=False,
    auth_user=None,
    auth_password=None,
    connection=None,
    html_message=None,
    text_message=None,
):
    template = get_template(template)
    content = template.render(context_data)
    if isinstance(recipient_list, str):
        recipient_list=[recipient_list]
    send_mail(
        subject=subject,
        message=text_message or content,
        recipient_list=recipient_list,
        from_email=from_email,
        fail_silently=fail_silently,
        auth_user=auth_user,
        auth_password=auth_password,
        connection=connection,
        html_message=content,
    )


def send_exception_email(exc):
    exc_info = sys.exc_info()
    subject = 'Exception Report'
    message = '\n'.join(traceback.format_exception(*exc_info))
    mail.mail_admins(
        subject, message, fail_silently=True,
        html_message=None
    )