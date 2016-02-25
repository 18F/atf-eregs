from django.core import management
from django.core.management.base import BaseCommand

from cfenv import AppEnv


class Command(BaseCommand):
    help = 'Migrate database and rebuild search index on cloud.gov'

    def handle(self, *args, **options):
        env = AppEnv()
        if env.index is None or env.index == 0:
            management.call_command('migrate', fake_initial=True)
            management.call_command('rebuild_index',
                                    interactive=False, remove=True)
