import os

import dj_database_url
from cfenv import AppEnv

from regcore.settings.pgsql import *  # noqa
from regcore.settings.pgsql import (  # explicitly referenced below
    INSTALLED_APPS, DATABASES)
REGCORE_APPS = tuple(INSTALLED_APPS)
REGCORE_DATABASES = dict(DATABASES)

from regulations.settings.base import *  # noqa
REGSITE_APPS = tuple(INSTALLED_APPS)

env = AppEnv()

# dedupe apps:
INSTALLED_APPS = ['overextends', 'atf_eregs']
INSTALLED_APPS.extend(a for a in REGCORE_APPS if a not in INSTALLED_APPS)
INSTALLED_APPS.extend(a for a in REGSITE_APPS if a not in INSTALLED_APPS)

DEBUG = os.environ.get('DEBUG', 'FALSE').upper() == 'TRUE'

ALLOWED_HOSTS = env.uris

ROOT_URLCONF = 'atf_eregs.urls'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join('.', 'eregs.db')
    )
}


def add_overextends(template):
    """Amend Django template engines to include the `overextends` tag"""
    if template['BACKEND'] == ('django.template.backends.django.'
                               'DjangoTemplates'):
        options = template['OPTIONS'] = template.get('OPTIONS', {})
        builtins = options['builtins'] = options.get('builtins', [])
        builtins.append('overextends.templatetags.overextends_tags')

    return template


TEMPLATES = [add_overextends(t) for t in TEMPLATES]

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
    'atf_eregs.sidebar.ATFResources',
    'atf_eregs.sidebar.Rulings',
    'regulations.generator.sidebar.help.Help',
)


USE_LIVE_DATA = os.environ.get('USE_LIVE_DATA', 'FALSE').upper() == 'TRUE'
if USE_LIVE_DATA:
    API_BASE = 'https://regulations.atf.gov/api/'
else:
    API_BASE = 'http://localhost:{}/api/'.format(
        os.environ.get('PORT', '8000'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s %(asctime)s %(name)-20s %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

# https://github.com/postgres/postgres/blob/c7b8998ebbf310a156aa38022555a24d98fdbfb4/src/backend/utils/adt/tsrank.c#L374
# seems to indicate that 1e-20 is a magic number; I'm not positive when it'd
# pop up, but in testing, the 1e-20 matches are bad (while 1e-19 can be
# "good"). Set the cutoff to 1e-20 so that we only return better results.
PG_SEARCH_RANK_CUTOFF = 1e-20


if DEBUG:
    CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
    CACHES['eregs_longterm_cache']['BACKEND'] = \
        'django.core.cache.backends.dummy.DummyCache'
    if not USE_LIVE_DATA:
        CACHES['api_cache']['TIMEOUT'] = 5  # roughly per request
