from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from CreateDatasetApp.forms import DatasetMetadataForm, DatasetSearchForm
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from CreateDatasetApp.table_creator import TableCreator
from UploadSource.models import SourceFile
from json import loads

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
    meta = DatasetMetadata.objects.filter(Q(metadata_id__exact=dataset_slug)).get()
    dataset = DatasetFile.objects.filter(metadata__metadata_id=meta.metadata_id)
    print(dataset)
    context = {
        'metadataForm': DatasetMetadataForm(),
        'object': dataset,
        'metadata' : meta,
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

    metadata_obj = DatasetMetadata.objects.create(
        name = metadata["name"],
        author = metadata["author"],
        keyValue = metadata["key_value"]
    )
    metadata_obj.tag.set(metadata["tags"])
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
