import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lab3.settings')

celery_app = Celery('lab3')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

@celery_app.task(blind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))