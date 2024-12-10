from json import loads
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from CreateDatasetApp.models import DatasetFile
from UploadSource.models import SourceFile


@require_POST
def save_list_by_pk(request, dataset_pk: int):

    # Check if dataset exists
    dataset = get_object_or_404(
        DatasetFile,
        pk=dataset_pk
    )

    # Check if sources exist
    pk_list = loads(request.POST.get("source_pks"))
    actual_sources = SourceFile.objects.filter(
        pk__in=pk_list
    )
    dataset.source_list.set(actual_sources)

    dataset.save()

    return HttpResponse()
