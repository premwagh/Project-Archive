from pathlib import Path
from environ import Env
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


Env.read_env(BASE_DIR.joinpath('.env'))
env = Env()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.str('DEBUG', 'false').lower() == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

BACKEND_ORIGIN = env.str(
    'BACKEND_ORIGIN', default="http://localhost:8000")
FRONTEND_ORIGIN = env.str(
    'FRONTEND_ORIGIN', default="http://localhost:3000")

# Host info
BACKEND_DOMAIN_NAME = env("BACKEND_DOMAIN_NAME", default=urlparse(BACKEND_ORIGIN).netloc.split(':')[0])
FRONTEND_DOMAIN_NAME = env("FRONTEND_DOMAIN_NAME", default=urlparse(FRONTEND_ORIGIN).netloc.split(':')[0])


