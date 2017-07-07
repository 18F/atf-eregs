import os

import dj_database_url
from cfenv import AppEnv

from regcore.settings.base import *  # noqa
from regcore.settings.base import (  # explicitly referenced below
    INSTALLED_APPS, DATABASES)
REGCORE_APPS = tuple(INSTALLED_APPS)
REGCORE_DATABASES = dict(DATABASES)

from regulations.settings.base import *  # noqa
REGSITE_APPS = tuple(INSTALLED_APPS)

env = AppEnv()

INSTALLED_APPS = ('overextends', 'atf_eregs',) + REGCORE_APPS + REGSITE_APPS

DEBUG = os.environ.get('DEBUG', 'FALSE').upper() == 'TRUE'

ALLOWED_HOSTS = env.uris

ROOT_URLCONF = 'atf_eregs.urls'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join('.', 'eregs.db')
    )
}

STATICFILES_DIRS = ['compiled']
STATIC_ROOT = os.environ.get('STATIC_ROOT', STATIC_ROOT)

DATA_LAYERS = (
    'regulations.generator.layers.defined.DefinedLayer',
    'regulations.generator.layers.definitions.DefinitionsLayer',
    'regulations.generator.layers.external_citation.ExternalCitationLayer',
    'regulations.generator.layers.footnotes.FootnotesLayer',
    'regulations.generator.layers.formatting.FormattingLayer',
    'regulations.generator.layers.internal_citation.InternalCitationLayer',
    'regulations.generator.layers.key_terms.KeyTermsLayer',
    'regulations.generator.layers.meta.MetaLayer',
    'regulations.generator.layers.paragraph_markers.ParagraphMarkersLayer',
    'regulations.generator.layers.toc_applier.TableOfContentsLayer',
    'regulations.generator.layers.graphics.GraphicsLayer',
)

SIDEBARS = (
    'atf_eregs.sidebar.Rulings',
    'regulations.generator.sidebar.help.Help',
)


USE_LIVE_DATA = 'DATABASE_URL' not in os.environ
if USE_LIVE_DATA:
    API_BASE = 'https://regulations.atf.gov/api/'
else:
    API_BASE = 'http://localhost:{}/api/'.format(
        os.environ.get('PORT', '8000'))

if DEBUG:
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
    CACHES['eregs_longterm_cache']['BACKEND'] = \
        'django.core.cache.backends.dummy.DummyCache'
    if not USE_LIVE_DATA:
        CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request
