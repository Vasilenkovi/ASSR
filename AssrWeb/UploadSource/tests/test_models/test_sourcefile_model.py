from django.test import TestCase
from django.db import IntegrityError
from UploadSource.models import SourceFile, SourceMetadata


class TestsSourceFile(TestCase):
    
    def test_blank_file(self):
        metadata = SourceMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )

        with self.assertRaises(IntegrityError):
            SourceFile.objects.create(
                metadata=metadata,
                ancestorFile=None
            )

    def test_save(self):
        metadata = SourceMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )

        file = SourceFile.objects.create(
            metadata=metadata,
            ancestorFile=b""
        )

        self.assertTrue(file.pk)
