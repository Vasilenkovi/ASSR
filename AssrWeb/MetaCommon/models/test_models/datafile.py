from django.db import models
from MetaCommon.models import DataFile
from .metadata import TestingMetadataModel


class TestingDataFile(DataFile):
    """Model to test DataFile abstract model"""

    objects = models.Manager()
    metadata = models.OneToOneField(
        TestingMetadataModel,
        null=True,
        on_delete=models.SET_NULL
    )