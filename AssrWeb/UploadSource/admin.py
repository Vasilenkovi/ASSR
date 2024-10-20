from django.contrib import admin
from UploadSource.models import SourceFile, SourceTags, SourceMetadata


@admin.register(SourceFile, SourceTags, SourceMetadata)
class SourceAdmin(admin.ModelAdmin):
    pass
