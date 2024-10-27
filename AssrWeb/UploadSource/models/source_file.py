from django.db import models
from MetaCommon.models import DataFile
from .source_file_meta import SourceMetadata


class SourceFile(DataFile):
    metadata = models.OneToOneField(
        SourceMetadata,
        null=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = False
