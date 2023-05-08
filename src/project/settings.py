from django.conf import settings
from rest_framework.settings import APISettings

PROJECT_SETTINGS = getattr(settings, 'PROJECT_SETTINGS', None)

DEFAULTS = {
    'PROJECT_GROUP_INVITE_TTL': 60 * 60 * 24 * 2,

}

# List of settings that may be in string import notation.
IMPORT_STRINGS = (
)

project_settings = APISettings(PROJECT_SETTINGS, DEFAULTS, IMPORT_STRINGS)
