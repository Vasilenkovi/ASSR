from django.urls import re_path
from UploadSource.consumer import UploadConsumer

websocket_urlpatterns = [
    re_path(r'ws/add-source-tag/', UploadConsumer.as_asgi())
]