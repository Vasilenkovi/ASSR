from django.db import models


class TransactionType(models.IntegerChoices):
    COLS = (0, "operate on column(s)")
    ROWS = (1, "operate on row(s)")
    CELL = (2, "operate on cell")
    SOURCE = (3, "operate on source files")