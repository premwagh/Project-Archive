from django.utils import timezone

from core.mailer import send_template_mail

from user.settings import user_settings

def send_email_verification(user):
    token = user.get_email_verification_token(
        ttl=user_settings.EMAIL_VERIFICATION_TOKEN_TTL,
    )
    link = user_settings.EMAIL_VERIFICATION_LINK_FORMAT.format(
        token=token,
        frontend_domain_name=user_settings.EMAIL_VERIFICATION_LINK_FRONTEND_DOMAIN_NAME,
    )
    send_template_mail(
        template="email/email-verification.html",
        context_data={
            'link': link,'full_name': user.get_full_name(),
            'ttl': user_settings.EMAIL_VERIFICATION_TOKEN_TTL,
        },
        subject="Supercrop - Email Verification.",
        recipient_list=user.email
    )

def send_password_reset(user):
    token = user.get_password_reset_token(
        ttl=user_settings.EMAIL_VERIFICATION_TOKEN_TTL,
    )
    link = user_settings.FORGOT_PASSWORD_RESET_LINK_FORMAT.format(
        token=token,
        frontend_domain_name=user_settings.FORGOT_PASSWORD_RESET_LINK_FRONTEND_DOMAIN_NAME,
    )
    send_template_mail(
        template="email/password-reset.html",
        context_data={
            'link': link,'full_name': user.get_full_name(),
            'ttl': user_settings.FORGOT_PASSWORD_RESET_TOKEN_TTL,
        },
        subject="Supercrop - Password Reset.",
        recipient_list=user.email
    )
