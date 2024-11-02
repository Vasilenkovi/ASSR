from django.shortcuts import render
from CreateDatasetApp.forms import DatasetMetadataForm, DatasetSearchForm
from UploadSource.models import SourceFile
from CreateDatasetApp.models import DatasetMetadata
from django.core.paginator import Paginator
from django.db.models import Q
from CreateDatasetApp.models import DatasetTags
# Create your views here.


def create_view(request):
    context = {
        "metadataForm": DatasetMetadataForm(),
        "source_files": SourceFile.objects.prefetch_related("metadata")
            .values("pk", "metadata__name", "metadata__author", "metadata__tag")
    }

    return render(request, "Datasets/create.html", context)


def show_list(request):
    search_form = DatasetSearchForm()
    search_query = request.GET.get('search_query', None)
    context = {
        'form': search_form,
        'page': 'Датасеты',
        'create_name': "Датасет",
    }
    selected_tags = request.GET.getlist('tags')
    print(search_query, selected_tags)
    if search_query is None and len(selected_tags) == 0:
        all_datasets = DatasetMetadata.objects.order_by('name')
        paginator = Paginator(all_datasets, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    else:
        search_result = DatasetMetadata.objects.filter(Q(name__contains=search_query))
        if search_query is not None and len(selected_tags) != 0:
            print("Tags_received")
            selected_tags = [i for i in DatasetTags.objects.filter(Q(name__in=selected_tags) )]
            print(selected_tags)
            search_result = DatasetMetadata.objects.filter(Q(name__contains=search_query) & Q(tag__in=selected_tags))
        paginator = Paginator(search_result, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
    return render(request, "Datasets/dataset-list.html", context)
