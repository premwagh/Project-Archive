import sys
from datetime import timedelta

from .base import env, SECRET_KEY


# TESTING CHECK
TESTING = 'test' in sys.argv or 'pytest' in sys.argv[0]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=365),
}

REST_USE_JWT = True


USER_SETTINGS = {
    "EMAIL_VERIFICATION_TOKEN_TTL": env.int("EMAIL_VERIFICATION_TOKEN_TTL", f"{60 * 60 * 24 * 2}"),
    "EMAIL_VERIFICATION_LINK_FORMAT": env.str(
        "EMAIL_VERIFICATION_LINK_FORMAT", "https://{frontend_domain_name}/auth/verify-email?code={token}"
    ),
    "FORGOT_PASSWORD_RESET_TOKEN_TTL": env.int("FORGOT_PASSWORD_RESET_TOKEN_TTL", f"{60 * 60 * 12}"),
    "FORGOT_PASSWORD_RESET_LINK_FORMAT": env.str(
        "FORGOT_PASSWORD_RESET_LINK_FORMAT", "https://{frontend_domain_name}/auth/reset-password?code={token}"
    ),
}