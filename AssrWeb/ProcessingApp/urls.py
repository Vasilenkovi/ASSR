from django.urls import path
from ProcessingApp.views import AcceptTaskView, launch_task


app_name = "proccessing"

urlpatterns = [
    path("new-proccess/", AcceptTaskView.as_view(), name="new-process"),
    path("dummy-task/", launch_task, name="dummy-task")
]
