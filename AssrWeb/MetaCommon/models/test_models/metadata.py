from django.db import models
from MetaCommon.models import Metadata
from .tags import TestingTagsModel


class TestingMetadataModel(Metadata):
    objects = models.Manager()
    tag = models.ManyToManyField(TestingTagsModel)