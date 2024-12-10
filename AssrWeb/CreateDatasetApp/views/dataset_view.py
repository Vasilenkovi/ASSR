from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Value
from django.http import HttpResponse
from django.db.models import Q
from CreateDatasetApp.forms import DatasetMetadataForm, DatasetSearchForm
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from MetaCommon import source_content_creator

def show_list(request):
    search_form = DatasetSearchForm()
    search_query = request.GET.get('search_query', None)
    context = {
        'form': search_form,
        'page': 'Датасеты',
        'create_name': "Датасет",
        'link': 'dataset:view_dataset',
        'addition_link': "dataset:new-source",
    }
    selected_tags = request.GET.getlist('tag')
    if search_query is None and len(selected_tags) == 0:
        all_datasets = DatasetMetadata.objects.order_by('name')
        paginator = Paginator(all_datasets, 8)
    else:
        search_result = DatasetMetadata.objects.filter(Q(name__contains=search_query))
        if search_query is not None and len(selected_tags) != 0:
            selected_tags = [i for i in DatasetTags.objects.filter(Q(pk__in=selected_tags))]
            search_result = DatasetMetadata.objects.filter(Q(name__contains=search_query) & Q(tag__in=selected_tags))
        paginator = Paginator(search_result, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, "Datasets/dataset-list.html", context)


def view_dataset(request, dataset_slug):
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    key_values = []
    for i in dataset.metadata.keyValue.keys():
        key_values.append({"key": i, "value": dataset.metadata.keyValue[i]})
    file = dataset.currentFile
    cc = source_content_creator.ContentCreator([file])
    table = cc.to_html_embed()
    context = {
        'form': DatasetMetadataForm(),
        'object': dataset,
        'key_value': key_values,
        'table': table,
        'source_files': dataset.source_list.all().annotate(checked=Value(True))
    }
    
    return render(request, "Datasets/dataset-view.html", context)


def dataset_download(request, dataset_slug):
    csv_file = get_object_or_404(DatasetFile, id=dataset_slug)
    response = HttpResponse(csv_file.currentFile, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{csv_file.metadata.name}.csv"'
    return response

