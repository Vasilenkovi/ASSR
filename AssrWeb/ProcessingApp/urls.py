from django.urls import path

from ProcessingApp.views import (
    List_Result_View,
    Guide_view,
    AcceptTaskView,
    task_results,
    download_processing_results
)

app_name = "processing"

urlpatterns = [
    path("new-process/", AcceptTaskView.as_view(), name="new-process"),
    path("view/<slug:task_pk>/", task_results, name="view"),
    path("view/<slug:task_pk>/download/", download_processing_results, name="download"),
    path("tasks/", List_Result_View.as_view(), name="task-list"),
    path("guide/", Guide_view.as_view(), name="guide"),
]
