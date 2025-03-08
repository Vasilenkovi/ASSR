from django.urls import path
from ProcessingApp.views import AcceptTaskView, List_Result_View, Guide_view


app_name = "processing"

urlpatterns = [
    path("new-process/", AcceptTaskView.as_view(), name="new-process"),
    path("tasks/", List_Result_View.as_view(), name="task-list"),
    path("guide/", Guide_view.as_view(), name="guide")
]
