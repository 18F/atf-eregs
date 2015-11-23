from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Analytics settings
ANALYTICS = {
    'GOOGLE': {
       'GTM_SITE_ID': '',
       'GA_SITE_ID': '',
    },
    'DAP': {
        'AGENCY': 'DOJ',
        'SUBAGENCY': 'ATF',
    },
}

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['eregs_longterm_cache']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request

try:
    from local_settings import *
except ImportError:
    pass
