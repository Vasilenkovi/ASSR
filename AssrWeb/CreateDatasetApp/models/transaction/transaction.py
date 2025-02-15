from django.db import models
from .transaction_type import TransactionType
from .transaction_direction import TransactionDirection
from CreateDatasetApp.models.dataset_file import DatasetFile

class Transaction(models.Model):
    description = models.TextField(
        null=True,
        verbose_name='Описание изменений транзакции',
        blank=True,
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='Дата создания'
    )
    transaction_type = models.IntegerField(
        choices=TransactionType.choices,
        verbose_name='Гранулярность транзакции (по столбцам, строкам, ячейкам, по файлам-исходникам)'
    )
    transaction_direction = models.IntegerField(
        choices=TransactionDirection.choices,
        verbose_name='Транзакция по удалению или изменению'
    )
    location = models.JSONField(
        verbose_name='Данные о столбце и/или строке, где произошло изменение'
    )
    data = models.JSONField(
        verbose_name='Новые данные, если происходило изменение или добавление',
        null=True
    )
    dataset = models.ForeignKey(
        DatasetFile,
        on_delete=models.CASCADE,
        verbose_name='Датасет к которому относится транзакция',
        blank=True
    )


    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(transaction_type__in=TransactionType.values),
                name="transaction_type_bound"
            ),
            models.CheckConstraint(
                check=models.Q(transaction_direction__in=TransactionDirection.values),
                name="transaction_direction_bound"
            )
        ]
