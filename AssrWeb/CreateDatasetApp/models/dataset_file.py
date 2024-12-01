from django.db import models
from MetaCommon.models import DataFile
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


    class Meta:
        abstract = False