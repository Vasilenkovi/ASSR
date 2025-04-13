from django.urls import path
from .api import visualization

app_name = "visual"

urlpatterns = [
    path(
        'results/<int:task_pk>/figures/',
        visualization.get_figures,
        name='get_figures'
    ),
]