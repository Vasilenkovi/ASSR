from django.db import models
from django.core import validators
from MetaCommon.models import DataFile, Tags, Metadata
# Create your models here.


class Transaction(models.Model):
    """
        Model of transaction performed on file
    """

    # actual values stored at db
    CELL = "Cel"
    LINE = "Lin"
    COLN = "Col"

    # django admin values
    OPERATION_CHOICES = (
        (CELL, "Cell"),
        (LINE, "Line"),
        (COLN, "Column"),
    )

    operation = models.CharField(
        max_length=3,
        choices=OPERATION_CHOICES,
        default=OPERATION_CHOICES[0],
        verbose_name='Операция'
    )

    id = models.AutoField(primary_key=True)
    creationDate = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата выполнения'
    )
    author = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator(50)],
        verbose_name='Автор'
    )
    description = models.CharField(
        max_length=255,
        validators=[validators.MaxLengthValidator(255)],
        verbose_name="Описание"
    )
    transactionData = models.JSONField()


class DatasetMetadataTagsModel(Tags):
    """
        Model of tags specificly used in Dataset's metadata\n
        a.k.a. for DatasetMetadata.
    """


class DatasetMetadata(Metadata):
    """
        Model of metadata created for DatasetFile
    """

    tag = models.ManyToManyField(DatasetMetadataTagsModel)


class DatasetFile(DataFile):
    """
        Abstract model of DasetFile to inherit from.
    """

    class Meta:
        abstract = True

    currentFile = models.BinaryField(verbose_name='Файл-текущий')
    transactions = models.ManyToManyField(Transaction)
    DatasetMetadata = models.OneToOneField(
        DatasetMetadata,
        on_delete=models.CASCADE
    )
