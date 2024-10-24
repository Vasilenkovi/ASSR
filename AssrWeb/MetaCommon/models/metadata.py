from django.db import models
from django.core import validators
from .tags import Tags


class Metadata(models.Model):
    name = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator(50)]
    )
    author = models.CharField(
        max_length=50,
        blank=True,
        validators=[validators.MaxLengthValidator(50)]
    )
    creationData = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        verbose_name='Дата создания'
    )
    keyValue = models.JSONField(blank=True)
    tag = models.ManyToManyField(Tags, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name