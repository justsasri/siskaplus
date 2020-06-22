from .base import *


DEBUG = False

INSTALLED_APPS = installed_apps

MIDDLEWARE = middleware

try:
    from .local import *
except ImportError:
    pass
