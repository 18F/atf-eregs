from .base import *     # noqa
from .base import CACHES    # explicitly referenced below

DEBUG = True

# Analytics settings

CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
CACHES['eregs_longterm_cache']['BACKEND'] = \
    'django.core.cache.backends.dummy.DummyCache'
CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request

try:
    from local_settings import *    # noqa
except ImportError:
    pass
