from base64 import urlsafe_b64encode
from django.conf import settings
from cryptography.fernet import Fernet

# creating global Fernet instance for encryption and decryption.
FERNET_KEY = (settings.SECRET_KEY * int(1 + 32//len(settings.SECRET_KEY)))[:32]
FERNET_KEY = urlsafe_b64encode((FERNET_KEY.encode('utf-8'))).decode('utf-8')
fernet = Fernet(FERNET_KEY)