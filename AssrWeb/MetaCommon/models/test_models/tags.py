from django.db import models
from MetaCommon.models import Tags


class TestingTagsModel(Tags):
    objects = models.Manager()