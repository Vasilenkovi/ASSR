from django.db import models
from MetaCommon.models import DataFile
from .dataset_file_meta import DatasetMetadata
from .transaction import Transaction


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
    transactions = models.ForeignKey(
        Transaction,
        null=True,
        on_delete=models.CASCADE
    )

    class Meta:
        abstract = False