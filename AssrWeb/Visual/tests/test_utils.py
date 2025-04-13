from unittest import TestCase

from CreateDatasetApp.models import DatasetFile, DatasetMetadata
from ProcessingApp.models import Processing_model
from UploadSource.models import SourceFile, SourceMetadata
from Visual.results import parser_factory, Text_Parser, Token_Parser
from Visual.results.utils import (
    MongoDB_Proxy,
    Task_Not_Supported_Error,
    Inference_Not_performed_Error
)


class Mock_MongoDB(MongoDB_Proxy):

    def find_one(self, in_pk: int) -> dict:
        return '{"processing_id": 1, "error_message": null, "files": []}'


class Test_Token_Parser(TestCase):

    def test_parser_factory(self):
        s_metadata = SourceMetadata.objects.create(
            name="file",
            author=None,
            keyValue=None
        )
        s_file = SourceFile.objects.create(
            metadata=s_metadata,
            ancestorFile=b""
        )

        d_metadata = DatasetMetadata.objects.create(
            name="test_name",
            author=None,
            keyValue=None
        )
        d_file = DatasetFile.objects.create(
            metadata=d_metadata,
            ancestorFile=b""
        )
        d_file.source_list.set([s_file])
        d_file.save()

        p_model = Processing_model.objects.create(
            dataset=d_file,
            model="test model"
        )

        with self.assertRaises(Inference_Not_performed_Error):
            parser_factory(p_model, Mock_MongoDB())

        p_model.task = Processing_model.Task.Text_class
        p_model.save()
        parser_1 = parser_factory(p_model, Mock_MongoDB())
        self.assertIs(
            type(parser_1),
            Text_Parser
        )

        p_model.task = Processing_model.Task.Token_class
        p_model.save()
        parser_2 = parser_factory(p_model, Mock_MongoDB())
        self.assertIs(
            type(parser_2),
            Token_Parser
        )
        
        p_model.task = Processing_model.Task.Other
        p_model.save()
        with self.assertRaises(Task_Not_Supported_Error):
            parser_factory(p_model, Mock_MongoDB())
