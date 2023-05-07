from os import (urandom,)
from base64 import b32encode
from django_otp.util import hex_validator, random_hex as org_random_hex


def key_validator(*args, **kwargs):
    """Wraps hex_validator generator, to keep makemigrations happy."""
    return hex_validator()(*args, **kwargs)

def random_hex(length=20):
    return org_random_hex(length=length)

def random_hex_32(length=32):
    return org_random_hex(length=length)

def static_token():
    return b32encode(urandom(5)).decode('utf-8').lower()

def phone_number_mask(phone_num_str):
    mask = phone_num_str
    if len(phone_num_str) > 8:
        if phone_num_str[0] == '+':
            mask = phone_num_str[0:3] + '*' * (len(phone_num_str) - 6) + phone_num_str[-3:]
        else:
            mask = phone_num_str[0:2] + '*' * (len(phone_num_str) - 4) + phone_num_str[-2:]
    return mask
