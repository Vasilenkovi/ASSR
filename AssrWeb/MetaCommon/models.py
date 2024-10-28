from django.db import models
from django.core import validators
# Create your models here.


class Tags(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator],
        unique=True
    )

    class Meta:
        abstract = True


class Metadata(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator(50)]
    )
    author = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator(50)]
    )
    creationData = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата создания'
    )
    keyValue = models.JSONField()
    tag = models.ManyToManyField(Tags)

    class Meta:
        abstract = True


class TestingTagsModel(Tags):
    objects = models.Manager()


class TestingMetadataModel(Metadata):
    objects = models.Manager()
    tag = models.ManyToManyField(TestingTagsModel)


class DataFile(models.Model):
    """
        Abstract model to inheret common fields and methods\n
        from.
    """

    class Meta:
        abstract = True

    ancestorFile = models.BinaryField(
        verbose_name='Файл-прородитель'
    )
    metadata = models.OneToOneField(
        Metadata,
        on_delete=models.CASCADE,
        verbose_name='Метадата'
    )

    def __str__(self) -> None:
        return self.metadata.name


class TestingDataFile(DataFile):
    """
        Model to test DataFile abstract model
    """

    objects = models.Manager()
    metadata = models.OneToOneField(
        TestingMetadataModel,
        on_delete=models.CASCADE
    )
