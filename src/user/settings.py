from django.conf import settings
from rest_framework.settings import APISettings

USER_SETTINGS = getattr(settings, 'USER_SETTINGS', None)

DEFAULTS = {
    # Email Verification Token TTL, in seconds
    'EMAIL_VERIFICATION_TOKEN_TTL': 60 * 60 * 24 * 2,

    'EMAIL_VERIFICATION_LINK_FORMAT': 'https://{frontend_origin}/auth/verify-email?code={token}',

    'EMAIL_VERIFICATION_LINK_FRONTEND_ORIGIN': settings.FRONTEND_ORIGIN,


    # Forgot Password Reset Token TTL, in seconds
    'FORGOT_PASSWORD_RESET_TOKEN_TTL': 60 * 60 * 12,

    'FORGOT_PASSWORD_RESET_LINK_FORMAT': '{frontend_origin}/reset-password?code={token}',

    'FORGOT_PASSWORD_RESET_LINK_FRONTEND_ORIGIN': settings.FRONTEND_ORIGIN,
}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
)

user_settings = APISettings(USER_SETTINGS, DEFAULTS, IMPORT_STRINGS)
