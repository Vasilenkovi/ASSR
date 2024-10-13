from django.db import models
from MetaCommon.models import Metadata
from .source_file_tag import SourceTags


class SourceMetadata(Metadata):
    
    class Meta:
        abstract = False

    tag = models.ManyToManyField(SourceTags)