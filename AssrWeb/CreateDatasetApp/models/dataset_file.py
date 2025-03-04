from django.db import models
from MetaCommon.models import DataFile
from UploadSource.models import SourceFile
from .dataset_file_meta import DatasetMetadata


class DatasetFile(DataFile):
    metadata = models.OneToOneField(
        DatasetMetadata,
        null=True,
        on_delete=models.CASCADE,
        related_name="dataset_file"
    )
    currentFile = models.BinaryField(
        max_length=1073741824,
        verbose_name='Актульная версия файла'
    )
    source_list = models.ManyToManyField(
        SourceFile,
        verbose_name="Текущий список источников",
        db_column='file_list',
        through='Dataset_Files'
    )
    ancestor_list = models.ManyToManyField(
        SourceFile,
        verbose_name="Изначальный список источников",
        related_name = "ancestor_list"
    )

    class Meta:
        abstract = False
        db_table = "dataset"


class Dataset_Files(models.Model):
    dataset = models.ForeignKey(
        DatasetFile,
        on_delete=models.CASCADE,
        db_column="dataset_id"
    )
    file = models.ForeignKey(
        SourceFile,
        on_delete=models.CASCADE,
        db_column="file_id"
    )
    
    class Meta:
        db_table = "dataset_files"
