import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_tutorial.settings")
django.setup()

from django.core.management import call_command

call_command('loaddata', 'data.json')