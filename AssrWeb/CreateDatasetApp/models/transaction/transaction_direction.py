from django.db import models


class TransactionDirection(models.IntegerChoices):
    CHANGE = (0, "add or modify value at location")
    REMOVE = (1, "delete value at location")
