from django.urls import path
from .views import upload_page_view, upload_endpoint_view, details_page_view 

app_name = "source"

urlpatterns = [
    path("new-source", upload_page_view, name="new-source"),
    path("file", upload_endpoint_view, name="file-upload"),
    path("details/<int:metadata_id>", details_page_view, name="details"),
]