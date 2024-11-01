from django.urls import path
from .views import create_view, table_view, table_save_view

app_name = "dataset"

urlpatterns = [
    path("new-dataset", create_view, name="new-source"),
    path("save", table_save_view, name="save"),
    path("table", table_view, name="table")
]