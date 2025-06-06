from django.test import TestCase
from django.db import IntegrityError
from CreateDatasetApp.models import DatasetFile, DatasetMetadata
from UploadSource.models import SourceFile, SourceMetadata


class TestsDatasetFile(TestCase):
    
    def test_blank_file(self):
        metadata = DatasetMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )

        with self.assertRaises(IntegrityError):
            DatasetFile.objects.create(
                metadata=metadata,
                ancestorFile=None
            )

    def test_save(self):
        metadata = DatasetMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )

        file = DatasetFile.objects.create(
            metadata=metadata,
            ancestorFile=b""
        )

        self.assertTrue(file.pk)

    def test_source_list_save(self):
        metadata_1 = SourceMetadata.objects.create(
            name="file_1",
            author=None,
            keyValue=None
        )
        file_1 = SourceFile.objects.create(
            metadata=metadata_1,
            ancestorFile=b""
        )

        metadata_2 = SourceMetadata.objects.create(
            name="file_2",
            author=None,
            keyValue=None
        )
        file_2 = SourceFile.objects.create(
            metadata=metadata_2,
            ancestorFile=b""
        )

        metadata = DatasetMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )
        file = DatasetFile.objects.create(
            metadata=metadata,
            ancestorFile=b""
        )
        file.source_list.set([file_1, file_2])
        file.save()

        self.assertEqual(len(file.source_list.all()), 2)
