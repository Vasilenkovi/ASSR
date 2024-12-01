from django.urls import path
from CreateDatasetApp.views import *

app_name = "dataset"

urlpatterns = [
    path("new-dataset", create_view, name="new-source"),
    path("save", table_save_view, name="save"),
    path("table", table_view, name="table"),
    path("new-dataset", create_view, name="new-source"),
    path("datasets-list", show_list, name="datasets-list"),
    path("datasets-list/<slug:dataset_slug>/", view_dataset, name="view_dataset"),
    path("dataset-deletion/<slug:dataset_slug>/", delete_dataset, name='deletion'),
    path("datasets-list/<slug:dataset_slug>/edit_cell/", edit_cell, name="edit_cell"),
    path("datasets-list/<slug:dataset_slug>/remove_row/", remove_row, name="edit_cell"),
    path("datasets-list/<slug:dataset_slug>/import_from/", import_from, name="edit_cell"),
    path("datasets-list/<slug:dataset_slug>/new_line/", new_line, name="edit_cell"),
    path("datasets-list/<slug:dataset_slug>/remove_column/", remove_column, name="edit_cell"),
    path("datasets-list/<slug:dataset_slug>/download/", dataset_download, name='dataset_download')
]
