from django.urls import re_path
from UploadSource.consumer import UploadConsumer

websocket_urlpatterns = [
    re_path(r'ws/socket-download-source/', UploadConsumer.as_asgi())
]