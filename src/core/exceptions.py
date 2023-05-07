from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidToken(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Invalid token.')
    default_code = 'invalid'

class ExpiredToken(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Expired token.')
    default_code = 'invalid'
