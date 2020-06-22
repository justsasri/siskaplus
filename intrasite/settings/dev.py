from .base import *


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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jx8vhpk-t$7tc$z1btb^!2n*f3i)%6bhdr@6&w8kiz@!v^c(ol'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
