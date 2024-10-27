from django.db import models
from .transaction_type import TransactionType
from .transaction_direction import TransactionDirection


class Transaction(models.Model):
    description = models.TextField(
        null=True,
        verbose_name='Описание изменений транзакции'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='Дата создания'
    )
    transaction_type = models.IntegerField(
        choices=TransactionType.choices,
        verbose_name='Гранулярность транзакции (по столбцам, строкам, ячейкам)'
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
