from django.urls import path
from ProcessingApp.views import AcceptTaskView


app_name = "proccessing"

urlpatterns = [
    path("new-proccess/", AcceptTaskView.as_view(), name="new-process"),
]
