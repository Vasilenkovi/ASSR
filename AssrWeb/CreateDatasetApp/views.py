from django.shortcuts import render
from CreateDatasetApp.forms import DatasetMetadataForm
from UploadSource.models import SourceFile


# Create your views here.
def create_view(request):
    context = {
        "metadataForm": DatasetMetadataForm(),
        "source_files": SourceFile.objects.prefetch_related("metadata")
            .values("pk", "metadata__name", "metadata__author", "metadata__tag")
    }

    return render(request, "Datasets/create.html", context)
