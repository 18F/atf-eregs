import json
import os

import dj_database_url

from .base import *

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


vcap_app = json.loads(os.environ.get('VCAP_APPLICATION', '{}'))
ALLOWED_HOSTS = ['localhost'] + vcap_app.get('application_uris', [])

vcap_services = json.loads(os.environ.get('VCAP_SERVICES', '{}'))
es_services = []
for service_name, services in vcap_services.items():
    if 'elasticsearch' in service_name:
        es_services.extend(services)

if es_services:
    HAYSTACK_CONNECTIONS['default'] = {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': es_services[0]['credentials']['uri'],
        'INDEX_NAME': 'eregs',
    }
