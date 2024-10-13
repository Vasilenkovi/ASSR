from django.urls import re_path
from CreateDatasetApp.consumer import CreationConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-download-source/', CreationConsumer.as_asgi())
]