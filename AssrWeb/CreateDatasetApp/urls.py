from django.urls import path
from CreateDatasetApp.views import *

app_name = "dataset"

urlpatterns = [
    path("new-dataset", create_view, name="new-source"),
    path("save", table_save_view, name="save"),
    path("table", table_view, name="table"),
    path("<int:dataset_pk>/save-source/", save_list_by_pk, name="save-source"),
    path("datasets-list", show_list, name="datasets-list"),
    # path(
    #     "datasets-list/<slug:dataset_slug>/",
    #     view_dataset,
    #     name="view_dataset"
    # ),
    path(
        "datasets-list/<slug:dataset_slug>/",
        Dataset_Details.as_view(),
        name="view_dataset"
    ),
    path("dataset-deletion/<slug:dataset_slug>/", delete_dataset, name='deletion'),
    path("datasets-list/<slug:dataset_slug>/edit_cell/", edit_cell, name="edit_cell"),
    path("datasets-list/<slug:dataset_slug>/remove_row/", remove_row, name="remove_row"),
    path("datasets-list/<slug:dataset_slug>/remove_column/", remove_column, name='remove_column'),
    path("datasets-list/<slug:dataset_slug>/import_from/", import_from, name="import_from"),
    path("datasets-list/<slug:dataset_slug>/new_line/", new_line, name="new_line"),
    path("datasets-list/<slug:dataset_slug>/remove_source/", delete_source, name="delete_source"),
    path("datasets-list/<slug:dataset_slug>/new_source/", new_source, name="new_source"),
    path("datasets-list/<slug:dataset_slug>/download/", dataset_download, name='dataset_download'),
    path("dataset/<slug:dataset_slug>/versions/", versions_list, name='versions_list'),
    path('version/<int:pk>/', version, name='version'),
    path('switch_version/<int:pk>/', switch_to_version, name='switch_to_version'),
    path("dataset/<slug:dataset_slug>/restore_init/", switch_to_init_version, name='restore_init'),
]
