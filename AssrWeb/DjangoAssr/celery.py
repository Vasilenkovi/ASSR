import os
from celery import Celery
from py_inference.tasks import infer


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAssr.settings')

app = Celery('DjangoAssr')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def infer_wrapper(processing_request_id: int):
    infer(processing_request_id)
