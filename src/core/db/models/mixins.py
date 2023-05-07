"""
Basic building mixins.
"""
import time
from django.db import models
from django.utils.translation import gettext_lazy as _

from cryptography.fernet import InvalidToken as CryptoInvalidToken

from core.exceptions import (InvalidToken, ExpiredToken)
from core.cryptography import fernet
from core.logging import logger


class TimeStampModelMixin(models.Model):
    """
    Mixin to add timestamp fields to a Model
    """
    created_on = models.DateTimeField(_('Created On'), auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(_('Updated On'),auto_now=True)

    class Meta:
        abstract = True



class TokenVerificationMixin(models.Model):
    """
    Mixin add token verification methods to a Model
    """
    def _get_token(self, context_fields, token_type, ttl):
        """
        Generate verification token.

        Args:
            context_fields (typing.Union[list[str], tuple[str]]): values of specified
                fields will be added to the token context.
            token_type (str): Unique string to identify token usage.
            ttl (int): Time to live fot the token in seconds.

        Raises:
            TypeError: if arg ttl in not of type int.

        Returns:
            str: Generated Token.
        """
        if not isinstance(ttl, int):
            raise TypeError(f'Inappropriate type: {type(ttl)} for ttl whereas a int is expected')
        context_ls = []
        for field in context_fields:
            context_ls.append(str(getattr(self, field)))
        context_ls.append(token_type)
        context_ls.append(str(ttl))
        context = "|".join(context_ls)
        token_bytes = fernet.encrypt(context.encode('utf-8'))
        # removing '=' to use token as url param
        return token_bytes.decode('utf-8').rstrip('=')

    @classmethod
    def _get_object_from_token(cls, context_fields, token_type, token):
        _MAX_CLOCK_SKEW = 60
        current_time = int(time.time())
        try:
            token_data = token + ('=' * (4 - len(token) % 4))
            token_data = token_data.encode('utf-8')

            timestamp = fernet.extract_timestamp(token_data)
            if current_time + _MAX_CLOCK_SKEW < timestamp:
                raise InvalidToken
            context = fernet.decrypt(token_data).decode('utf-8')
            context_ls = context.split('|')
            ttl = int(context_ls[-1])
            if timestamp + ttl < current_time:
                raise ExpiredToken
            if not context_ls[-2] == token_type:
                raise InvalidToken
            if len(context_ls[:-2]) != len(context_fields):
                raise InvalidToken
            lookup_kwargs = dict(zip(context_fields, context_ls[:-2]))
            try:
                obj = cls.objects.get(**lookup_kwargs)
            except cls.DoesNotExist as e:
                raise InvalidToken from e

        except CryptoInvalidToken as e:
            raise InvalidToken from e
        except (InvalidToken, ExpiredToken) as e:
            raise e from e
        except Exception as e:
            logger.exception(e)
            raise InvalidToken from e
        else:
            return obj

    class Meta:
        abstract = True
