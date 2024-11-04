from django.db import models
from django.core import validators
from .tags import Tags


class Metadata(models.Model):
    metadata_id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=50,
        validators=[validators.MaxLengthValidator(50)]
    )
    author = models.CharField(
        max_length=50,
        null=True,
        validators=[validators.MaxLengthValidator(50)]
    )
    creationData = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name='Дата создания'
    )
    keyValue = models.JSONField(null=True)
    tag = models.ManyToManyField(Tags)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name