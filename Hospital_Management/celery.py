# yourproject/celery.py
import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hospital_Management.settings')

app = Celery('Hospital_Management')

# Use a string here to make sure the worker doesn't serialize the object.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
