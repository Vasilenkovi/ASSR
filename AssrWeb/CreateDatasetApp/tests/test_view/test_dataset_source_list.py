from json import dumps
from django.test import RequestFactory, TestCase
from CreateDatasetApp.models import DatasetFile, DatasetMetadata
from CreateDatasetApp.views import save_list_by_pk
from UploadSource.models import SourceFile, SourceMetadata


class TestDatasetSourceList(TestCase):

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
        
        factory = RequestFactory()
        request = factory.post(
            f"/{file.pk}/save-source/",
            {
                "source_pks": dumps(
                    [file_1.pk, file_2.pk]
                )
            }
        )

        save_list_by_pk(request, file.pk)

        # Check if view has modified list
        file = DatasetFile.objects.get(pk=file.pk)
        self.assertEqual(len(file.source_list.all()), 2)
