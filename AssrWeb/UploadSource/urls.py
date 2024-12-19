from django.urls import path
from .views import (
    upload_page_view,
    upload_endpoint_view,
    filter_source_view,
    list_page_view,
    details_page_view,
    delete_view,
    Details_page,
)

app_name = "source"

urlpatterns = [
    path("new-source", upload_page_view, name="new-source"),
    path("file", upload_endpoint_view, name="file-upload"),
    path("filter-source-list", filter_source_view, name="filter-source-list"),
    path("source-list", list_page_view, name="source-list"),
    path("source-list/<int:metadata_id>", details_page_view, name="details"),
    path("source-deletion/<int:metadata_id>", delete_view, name="delete"),
    path(
        "call-file/<int:metadata_id>",
        view=Details_page.as_view(),
        name="callajax"
    ),
]
