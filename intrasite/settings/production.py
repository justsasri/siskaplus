import django_heroku
import dj_database_url

from .base import *
from .auth import *
from .cache import *

DEBUG = False

DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

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
