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
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Метадата'
    )

    def __str__(self) -> None:
        return self.metadata.name