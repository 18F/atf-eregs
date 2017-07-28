from django.core.management.base import BaseCommand

from atf_eregs.atf_resources import fetch_and_save_resources


class Command(BaseCommand):
    help = 'Load "Additional Resources" data from atf.gov'

    def handle(self, *args, **options):
        fetch_and_save_resources()
