import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'toy_shop.settings')
app = Celery('toy_shop')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

