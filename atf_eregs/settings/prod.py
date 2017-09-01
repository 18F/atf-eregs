import re

from cfenv import AppEnv

from .base import *  # noqa
from .base import CACHES, HAYSTACK_CONNECTIONS  # explicitly referenced below

def _limit_caches(max_timeout):
    """While the regulation content doesn't change often, we want to allow ATF
    to update their "Related Documents" relatively quickly."""
    for cache in CACHES.values():
        current_timeout = cache.get('TIMEOUT', 300)     # Django's default
        cache['TIMEOUT'] = min(current_timeout, max_timeout)

_limit_caches(60*60)    # 1 hour


DEBUG = False
TEMPLATE_DEBUG = False
ANALYTICS = {
    'GOOGLE': {
        'GTM_SITE_ID': '',
        'GA_SITE_ID': 'UA-48605964-38',
    },
    'DAP': {
        'AGENCY': 'DOJ',
        'SUBAGENCY': 'ATF',
    },
}

env = AppEnv()

HTTP_AUTH_USER = env.get_credential('HTTP_AUTH_USER')
HTTP_AUTH_PASSWORD = env.get_credential('HTTP_AUTH_PASSWORD')

ALLOWED_HOSTS = ['localhost'] + env.uris


try:
    from local_settings import *    # noqa
except ImportError:
    pass
