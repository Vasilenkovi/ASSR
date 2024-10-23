from django.urls import path
from .views import upload_page_view, upload_endpoint_view

app_name = "source"

urlpatterns = [
    path("new-source", upload_page_view, name="new-source"),
    path("file", upload_endpoint_view, name="file-upload")
]