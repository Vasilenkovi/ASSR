from django.db import models
from .metadata import Metadata


class DataFile(models.Model):
    """
        Abstract model to inheret common fields and methods\n
        from.
    """

    class Meta:
        abstract = True

    # Max file length of 1 GB according to Postgres column limit
    ancestorFile = models.BinaryField(
        max_length=1073741824,
        verbose_name='Файл-прородитель'
    )
    metadata = models.OneToOneField(
        Metadata,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Метадата'
    )
    creationDate = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='Дата создания'
    )

    def __str__(self) -> None:
        return self.metadata.name
