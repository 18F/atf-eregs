import re

from cfenv import AppEnv

from .base import *  # noqa
from .base import HAYSTACK_CONNECTIONS  # explicitly referenced below

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
