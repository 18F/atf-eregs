import logging
import time

from django.core.management.base import BaseCommand

from atf_eregs.atf_resources import fetch_and_save_resources

logger = logging.getLogger(__name__)


def infinite_loop():
    """Allow a hook for tests, etc. to break the infinite loop."""
    return True


class Command(BaseCommand):
    help = 'Load "Additional Resources" data from atf.gov'

    def add_arguments(self, parser):
        parser.add_argument(
            '--period', type=int, help='Period of repetition, in seconds')

    def handle(self, *args, **options):
        while infinite_loop():
            prev_run = time.time()
            try:
                fetch_and_save_resources()
            except (IOError, ConnectionError):
                logger.exception('Error retrieving data')

            if options.get('period') is None:
                break

            next_run = prev_run + options['period']
            # Use `max` to account for running too long
            time.sleep(max(0, next_run - time.time()))
