from json import loads
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseBadRequest
from CreateDatasetApp.forms import DatasetMetadataForm
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from UploadSource.models import SourceFile
from UploadSource.views import _get_paginated_source_files
from .utils import _create_table


def create_view(request):
    context = {
        "metadataForm": DatasetMetadataForm(),
        "source_files": _get_paginated_source_files(
            "",
            1
        )
    }

    return render(request, "Datasets/create.html", context)


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
    actual_sources = SourceFile.objects.filter(
        pk__in=pk_list
    )
    dataset_obj.source_list.set(actual_sources)
    
    dataset_obj.save()

    response = {
        "dataset_id": dataset_obj.pk
    }

    return JsonResponse(response)
