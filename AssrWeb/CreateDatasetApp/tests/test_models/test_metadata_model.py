from django.test import TestCase
from django.db import IntegrityError
from CreateDatasetApp.models import DatasetMetadata, DatasetTags


class TestsSourceMetadata(TestCase):

    def test_blank(self):
        with self.assertRaises(IntegrityError):
            DatasetMetadata.objects.create(
                name=None,
                author="author",
                keyValue={"key": "value"}
            )

    def test_save(self):
        tag = DatasetTags.objects.create(
            name="test_name"
        )
        metadata = DatasetMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )
        metadata.tag.set([tag])

        self.assertTrue(metadata.pk)
        self.assertTrue(metadata.tag)
