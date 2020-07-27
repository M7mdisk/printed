# purge_old_data.py

from django.core.management.base import BaseCommand, CommandError
from shops.models import Order 
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Delete objects older than 100 days'

    def handle(self, *args, **options):
        for order in Order.objects.filter(date__lte=datetime.now()-timedelta(days=100)): 
            order.docfile.delete()
            self.stdout.write(f'Deleted order {order} older than 100 days')
        self.stdout.write('Deleted objects older than 100 days')