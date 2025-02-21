from django.shortcuts import render
from django.http import HttpResponse
from ProcessingApp.models import Processing_model
from django.views.generic.edit import CreateView
from DjangoAssr.celery import infer_wrapper


class AcceptTaskView(CreateView):
    model = Processing_model
    fields = ['dataset', 'model', 'parameters']
    template_name = 'Proccessing/create.html'


def launch_task(request):
    # Sends message to launch inference task on processing__id == 1
    infer_wrapper.delay(1)

    return HttpResponse("ok")
