import humanize
from django.db.models import F
from django.utils import timezone
from django.views.generic.list import ListView
from DjangoAssr.settings import PER_PAGE
from ProcessingApp.models import Processing_model


class List_Result_View(ListView):
    model = Processing_model
    fields = ('pk', 'dataset', 'model', 'parameters', 'status', 'creationTime')
    template_name = 'Proccessing/list.html'
    context_object_name = "task_list"
    paginate_by = PER_PAGE

    def get_queryset(self):
        queryset = Processing_model.objects.prefetch_related(
            "dataset"
        )

        return queryset
