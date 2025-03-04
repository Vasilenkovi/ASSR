from django.urls import reverse_lazy
from ProcessingApp.forms import Processing_Form
from django.views.generic.edit import CreateView
from DjangoAssr.celery import infer_wrapper


class AcceptTaskView(CreateView):
    form_class = Processing_Form
    template_name = 'Proccessing/create.html'
    success_url = reverse_lazy("processing:task-list")

    def form_valid(self, form):
        response = super(AcceptTaskView, self).form_valid(form)
        processing_record = form.instance
        infer_wrapper.delay(processing_record.pk)

        return response
