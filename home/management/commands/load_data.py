from django.core.management.base import BaseCommand
from django.core.management import call_command
from home.models import Departments
import os

class Command(BaseCommand):
    help = 'Load departments'

    def handle(self, *args, **kwargs):

        if Departments.objects.exists():
            self.stdout.write(self.style.WARNING('Departments already loaded'))
            return

        if os.path.exists('departments.json'):
            call_command('loaddata', 'departments.json')
            self.stdout.write(self.style.SUCCESS('Departments loaded'))
        else:
            self.stdout.write(self.style.ERROR('departments.json not found'))