from django.contrib import admin
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags


@admin.register(DatasetFile, DatasetMetadata, DatasetTags)
class DatasetAdmin(admin.ModelAdmin):
    pass
