from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Load initial data'

    def handle(self, *args, **kwargs):

        if os.path.exists('data.json'):
            call_command('loaddata', 'data.json')
            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
        else:
            self.stdout.write(self.style.ERROR('data.json not found'))