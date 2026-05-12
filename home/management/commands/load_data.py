from django.core.management.base import BaseCommand
from django.core.management import call_command
from home.models import Departments
import os

class Command(BaseCommand):
    help = 'Load initial data safely'

    def handle(self, *args, **kwargs):

        # Prevent duplicate loading
        if Departments.objects.exists():
            self.stdout.write(self.style.WARNING('Data already exists'))
            return

        if os.path.exists('data.json'):
            call_command('loaddata', 'data.json')
            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
        else:
            self.stdout.write(self.style.ERROR('data.json not found'))