import os

import newrelic.agent
from cfenv import AppEnv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atf_eregs.settings")
# important that the whitenoise import is after the line above
from whitenoise.django import DjangoWhiteNoise

env = AppEnv()

settings = newrelic.agent.global_settings()
settings.app_name = env.get_credential('NEW_RELIC_APP_NAME')
settings.license_key = env.get_credential('NEW_RELIC_LICENSE_KEY')
newrelic.agent.initialize()

application = DjangoWhiteNoise(get_wsgi_application())
