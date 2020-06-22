import django_heroku

from .base import *
from .auth import *
from .cache import *

DEBUG = False

INSTALLED_APPS = installed_apps

MIDDLEWARE = middleware

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Activate Django-Heroku.
django_heroku.settings(locals())

try:
    from .local import *
except ImportError:
    pass
