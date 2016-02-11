import re

import dj_database_url
from cfenv import AppEnv

from .base import *  # noqa

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

DATABASES = {
    'default': dj_database_url.config()
}

env = AppEnv()

HTTP_AUTH_USER = env.get_credential('HTTP_AUTH_USER')
HTTP_AUTH_PASSWORD = env.get_credential('HTTP_AUTH_PASSWORD')

ALLOWED_HOSTS = ['localhost'] + env.uris

# Service name may well change in the future. Fuzzy match
elastic_service = env.get_service(name=re.compile('search'))
if elastic_service:
    HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': elastic_service.credentials['uri'],
        'INDEX_NAME': 'eregs',
    }
