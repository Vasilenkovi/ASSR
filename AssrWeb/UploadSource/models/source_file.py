from django.db import models
from .source_file_meta import SourceMetadata


class SourceFile(models.Model):
    metadata = models.OneToOneField(SourceMetadata)
    # Max file length of 1 GB according to Postgres column limit
    init_file = models.BinaryField(max_length=1073741824)