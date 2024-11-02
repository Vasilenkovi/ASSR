from django.urls import path
from .views import create_view, show_list

app_name = "dataset"

urlpatterns = [
    path("new-dataset", create_view, name="new-source"),
    path("datasets-list", show_list, name="datasets-list"),
    #path("datasets-list/<slug:dataset_slug>/")
]