from json import loads
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from CreateDatasetApp.forms import DatasetMetadataForm, DatasetSearchForm
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from CreateDatasetApp.table_creator import TableCreator
from UploadSource.models import SourceFile
from UploadSource.views import _get_paginated_source_files
from MetaCommon import  source_content_creator

# Create your views here.


def create_view(request):
    context = {
        "metadataForm": DatasetMetadataForm(),
        "source_files": _get_paginated_source_files(
            "",
            1
        )
    }

    return render(request, "Datasets/create.html", context)


def show_list(request):
    search_form = DatasetSearchForm()
    search_query = request.GET.get('search_query', None)
    context = {
        'form': search_form,
        'page': 'Датасеты',
        'create_name': "Датасет",
        'link': 'dataset:view_dataset'
    }
    selected_tags = request.GET.getlist('tags')
    print(search_query, selected_tags)
    if search_query is None and len(selected_tags) == 0:
        all_datasets = DatasetMetadata.objects.order_by('name')
        paginator = Paginator(all_datasets, 8)
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


def view_dataset(request, dataset_slug):
    dataset = DatasetFile.objects.filter(metadata__metadata_id=dataset_slug).get()
    key_values = []
    for i in dataset.metadata.keyValue.keys():
        key_values.append({"key": i, "value": dataset.metadata.keyValue[i]})
    file = dataset.ancestorFile
    cc = source_content_creator.ContentCreator([file])
    table = cc.to_html_embed()
    context = {
        'form': DatasetMetadataForm(),
        'object': dataset,
        'key_value': key_values,
        'table': table,
    }
    return render(request, "Datasets/dataset-view.html", context)


@require_POST
def table_view(request):
    pk_list = loads(request.POST["pks"])

    if not pk_list:
        return HttpResponseBadRequest("no files selected")

    tc = _create_table(pk_list)
    response = {
        "html_table": tc.to_html()
    }

    return JsonResponse(response)


@require_POST
def table_save_view(request):
    pk_list = loads(request.POST["source_pks"])

    if not pk_list:
        return HttpResponseBadRequest("no files selected")

    metadata = loads(request.POST["metadata"])

    if not metadata["name"]:
        return HttpResponseBadRequest("Name should not be blank")

    tags = DatasetTags.objects.filter(
        name__in=metadata["tags"]
    )
    metadata_obj = DatasetMetadata.objects.create(
        name=metadata["name"],
        author=metadata["author"],
        keyValue=metadata["key_value"]
    )
    metadata_obj.tag.set(tags)
    metadata_obj.save()

    tc = _create_table(pk_list)
    bytes_obj = tc.to_csv().read()
    dataset_obj = DatasetFile.objects.create(
        ancestorFile=bytes_obj,
        currentFile=bytes_obj,
        metadata=metadata_obj
    )
    response = {
        "dataset_id": dataset_obj.pk
    }

    return JsonResponse(response)


def _create_table(pk_list: list[int]) -> TableCreator: 
    file_objs = SourceFile.objects.filter(
        pk__in=pk_list
    ).values("ancestorFile")
    file_bytes = [file["ancestorFile"] for file in file_objs]
    return TableCreator(file_bytes)

def delete_dataset(request, dataset_slug):
    DatasetFile.objects.filter(metadata__metadata_id=dataset_slug).get().delete()
    DatasetMetadata.objects.filter(metadata_id=dataset_slug).get().delete()
    return redirect('dataset:datasets-list')