from django.urls import re_path
from CreateDatasetApp.consumer import DatasetConsumer

websocket_urlpatterns = [
    re_path(r'ws/add-dataset-tag/', DatasetConsumer.as_asgi())
]