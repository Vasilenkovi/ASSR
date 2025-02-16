from django.db import models
from MetaCommon.models import DataFile
from UploadSource.models import SourceFile
from .dataset_file_meta import DatasetMetadata


class DatasetFile(DataFile):
    metadata = models.OneToOneField(
        DatasetMetadata,
        null=True,
        on_delete=models.CASCADE
    )
    currentFile = models.BinaryField(
        max_length=1073741824,
        verbose_name='Актульная версия файла'
    )
    source_list = models.ManyToManyField(
        SourceFile,
        verbose_name="Текущий список источников"
    )
    ancestor_list = models.ManyToManyField(
        SourceFile,
        verbose_name="Изначальный список источников",
        related_name = "ancestor_list"
    )

    class Meta:
        abstract = False