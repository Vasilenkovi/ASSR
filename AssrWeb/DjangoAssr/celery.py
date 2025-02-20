import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAssr.settings')

app = Celery('DjangoAssr')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task(name="inference.celery.infer_wrapper")
def infer_wrapper(processing_request_id: int):
    pass
