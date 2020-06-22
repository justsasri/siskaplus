import environ

from .base import *
from .auth import *
from .cache import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = [
    '127.0.0.1',
]

INSTALLED_APPS = [
    'django_extensions',
] + installed_apps + [
    # 'debug_toolbar'
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
] + middleware

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

try:
    from .local import *
except ImportError:
    pass
