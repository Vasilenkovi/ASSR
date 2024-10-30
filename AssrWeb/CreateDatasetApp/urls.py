from django.urls import path
from .views import create_view

app_name = "dataset"

urlpatterns = [
    path("new-dataset", create_view, name="new-source")
]