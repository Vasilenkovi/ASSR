from django.db import models

from CreateDatasetApp.models import DatasetFile


class Processing_model(models.Model):
    """Processing model."""

    class Status(models.TextChoices):
        """Class with Processing_model statuses,
         needed to make choices in status feild."""
        Cre = "0", "Created"
        Run = "1", "Running"
        Suc = "2", "Successed"
        Fai = "3", "Failed"

    dataset = models.ForeignKey(
        DatasetFile,
        on_delete=models.CASCADE,
        db_column='dataset_id' # Explicit column name for integration 
    )
    model = models.CharField(
        max_length=256,
        verbose_name='Имя модели обработки',
        db_column='model_name' # Explicit column name for integration 
    )
    parameters = models.JSONField(
        verbose_name='Опциональные параметры модели',
        db_column='extra_parameters' # Explicit column name for integration 
    )
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.Cre,
        verbose_name='Статус',
        db_column='status' # Explicit column name for integration 
    )
    creationTime = models.DateField(
        auto_now_add=True,
        verbose_name='Временная отметка создания запроса'
    )

    class Meta:
        db_table = "processing" # Explicit table name for integration 
