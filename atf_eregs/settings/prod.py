import json
import os

from .base import *

DEBUG = False
TEMPLATE_DEBUG = False

vcap = json.loads(os.environ.get('VCAP_APPLICATION', '{}'))
ALLOWED_HOSTS = ['localhost'] + vcap.get('application_uris', [])
