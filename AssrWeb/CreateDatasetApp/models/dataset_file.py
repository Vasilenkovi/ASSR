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
        verbose_name="Список источников",
        db_column='file_list',
        through='Dataset_Files'
    )

    class Meta:
        abstract = False
        db_table = "dataset"


class Dataset_Files(models.Model):
    dataset = models.ForeignKey(DatasetFile, on_delete=models.CASCADE)
    file = models.ForeignKey(SourceFile, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "dataset_files"
