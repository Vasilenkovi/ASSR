from django.shortcuts import render
from ProcessingApp.models import Processing_model
from django.views.generic.edit import CreateView


class AcceptTaskView(CreateView):
    model = Processing_model
    fields = ['dataset', 'model', 'parameters']
    template_name = 'Proccessing/create.html'
