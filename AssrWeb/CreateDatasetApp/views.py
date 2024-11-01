from io import BytesIO
from json import loads
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.http import require_POST
from CreateDatasetApp.forms import DatasetMetadataForm
from CreateDatasetApp.models import DatasetFile, DatasetMetadata
from CreateDatasetApp.table_creator import TableCreator
from UploadSource.models import SourceFile


# Create your views here.
def create_view(request):
    context = {
        "metadataForm": DatasetMetadataForm(),
        "source_files": SourceFile.objects.prefetch_related("metadata")
            .values("pk", "metadata__name", "metadata__author", "metadata__tag")
    }

    return render(request, "Datasets/create.html", context)


@require_POST
def table_view(request):
    pk_list = loads(request.POST["pks"])

    if not pk_list:
        return HttpResponseBadRequest("no files selected")

    tc = create_table(pk_list)
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
    metadata_obj = DatasetMetadata.objects.create(
        name = metadata["name"],
        author = metadata["author"],
        keyValue = metadata["key_value"]
    )
    metadata_obj.tag.set(metadata["tags"])
    metadata_obj.save()

    tc = create_table(pk_list)
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


def create_table(pk_list: list[int]) -> TableCreator: 
    file_objs = SourceFile.objects.filter(
        pk__in=pk_list
    ).values("ancestorFile")
    file_bytes = [file["ancestorFile"] for file in file_objs]

    return TableCreator(file_bytes)