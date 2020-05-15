import hashlib
from urllib import parse
from django.utils import translation

_ = translation.ugettext_lazy
AVATAR_DEFAULT = '//www.gravatar.com/avatar/?s=288&d=mm'


def get_gravatar_url(email, size=144):
    default = "mm"
    size = int(size) * 2  # requested at retina size by default and scaled down at point of use with css
    gravatar_provider_url = '//www.gravatar.com/avatar'

    if (not email) or (gravatar_provider_url is None):
        return None

    gravatar_url = "{gravatar_provider_url}/{hash}?{params}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip('/'),
        hash=hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
        params=parse.urlencode({'s': size, 'd': default})
    )
    return gravatar_url


def get_user_gravatar(user=None):
    if not user:
        return AVATAR_DEFAULT
    return get_gravatar_url(user.email)


def get_gravatar_profile(email):
    gravatar_provider_url = '//www.gravatar.com/'
    if (not email) or (gravatar_provider_url is None):
        return None
    gravatar_url = "{gravatar_provider_url}/{hash}".format(
        gravatar_provider_url=gravatar_provider_url.rstrip('/'),
        hash=hashlib.md5(email.lower().encode('utf-8')).hexdigest(),
    )
    return gravatar_url
