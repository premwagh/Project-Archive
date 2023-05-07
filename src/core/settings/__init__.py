from .base import ( # pylint: disable=W0611
    SECRET_KEY,
    DEBUG,
    BACKEND_ORIGIN,
    FRONTEND_ORIGIN,
    BACKEND_DOMAIN_NAME,
    FRONTEND_DOMAIN_NAME,
)
from .django import *
from .application import *
from .swagger import *