from django.test import TestCase
from django.db import IntegrityError
from UploadSource.models import SourceMetadata, SourceTags


class TestsSourceMetadata(TestCase):

    def test_blank(self):
        with self.assertRaises(IntegrityError):
            SourceMetadata.objects.create(
                name=None,
                author="author",
                keyValue={"key": "value"}
            )

    def test_save(self):
        tag = SourceTags.objects.create(
            name="test_name"
        )
        metadata = SourceMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )
        metadata.tag.set([tag])

        self.assertTrue(metadata.pk)
        self.assertTrue(metadata.tag)
