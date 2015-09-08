import json
import os

from regulations.settings.base import *

INSTALLED_APPS = ('atf_eregs',) + INSTALLED_APPS

DEBUG = False
TEMPLATE_DEBUG = False

vcap = json.loads(os.environ.get('VCAP_APPLICATION', '{}'))
ALLOWED_HOSTS = vcap.get('application_uris', [])
