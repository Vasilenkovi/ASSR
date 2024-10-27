from django.db import models
from MetaCommon.models import Metadata
from .dataset_file_tag import DatasetTags


class DatasetMetadata(Metadata):
    
    class Meta:
        abstract = False

    tag = models.ManyToManyField(DatasetTags)