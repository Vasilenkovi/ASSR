from django.db import models
from django.core import validators


class Tags(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator],
        unique=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name