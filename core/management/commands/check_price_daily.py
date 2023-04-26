from django.core.management.base import BaseCommand
from core.views import check_price_daily


class Command(BaseCommand):
    help = 'Runs the check_price function daily'

    def handle(self, *args, **options):
        check_price_daily()
