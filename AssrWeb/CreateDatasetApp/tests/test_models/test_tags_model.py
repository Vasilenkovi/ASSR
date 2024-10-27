from django.test import TestCase
from django.db import IntegrityError
from CreateDatasetApp.models import DatasetTags


class TestsDatasetTags(TestCase):

    def test_blank(self):
        with self.assertRaises(IntegrityError):
            DatasetTags.objects.create(name=None)

    def test_unique(self):
        tag = DatasetTags.objects.create(name="tag_name_1")
        self.assertTrue(tag.pk)

        with self.assertRaises(IntegrityError):
            DatasetTags.objects.create(name="tag_name_1")
