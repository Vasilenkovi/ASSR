from django.shortcuts import redirect
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags


def delete_dataset(request, dataset_slug):
    DatasetFile.objects.filter(metadata__pk=dataset_slug).get().delete()
    DatasetMetadata.objects.filter(pk=dataset_slug).get().delete()
    return redirect('dataset:datasets-list')