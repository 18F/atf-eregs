import os

import newrelic.agent
from cfenv import AppEnv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atf_eregs.settings")
# important that the whitenoise import is after the line above
from whitenoise.django import DjangoWhiteNoise  # noqa

env = AppEnv()
app_name = env.get_credential('NEW_RELIC_APP_NAME')
license_key = env.get_credential('NEW_RELIC_LICENSE_KEY')

if app_name and license_key:
    settings = newrelic.agent.global_settings()
    settings.app_name = app_name
    settings.license_key = license_key
    newrelic.agent.initialize()

application = DjangoWhiteNoise(get_wsgi_application())
