from django.test import TestCase
from MetaCommon.models import TestingTagsModel, TestingMetadataModel
from MetaCommon.models import TestingDataFile
import datetime


class MetadataTest(TestCase):    # TODO make it better

    def setUp(self):
        self.correctMetadataData = {
            "name": "MetaDataName",
            "author": "Someone",
            "keyValue": {"key1": "value1", "key2": "value2"},
            "keyValueJSON": """ {"key1": "value1", "key2": "value2" } """,
            "tags": ["tag1", "tag2", "tag3"]
        }
        self.metadataDict = TestingMetadataModel.objects.create(
            name=self.correctMetadataData["name"],
            author=self.correctMetadataData["author"],
            keyValue=self.correctMetadataData["keyValue"]
        )
        for t in self.correctMetadataData["tags"]:
            tag = TestingTagsModel.objects.create(name=t)
            self.metadataDict.tag.add(tag)

        self.correctDataFileData = {
            "title": "NewTestDataFile",
            "ancestorFile": b'1010101010',
            "metadata": self.metadataDict
        }
        self.incorrectDataFileData = {
            "title": None,
            "ancestorFile": None,
            "metadata": "Something wrong"
        }
        self.datafile = TestingDataFile.objects.create(
            title=self.correctDataFileData["title"],
            ancestorFile=self.correctDataFileData["ancestorFile"],
            metadata=self.correctDataFileData["metadata"]
        )

    def testDataTypes(self):
        self.assertEqual(
            type(self.datafile.title),
            type(self.correctDataFileData["title"])
        )
        self.assertEqual(
            type(self.datafile.ancestorFile),
            type(self.correctDataFileData["ancestorFile"])
        )
        self.assertEqual(
            type(self.datafile.metadata),
            type(self.correctDataFileData["metadata"])
        )
        self.assertEqual(
            type(self.datafile.creationDate),
            type(datetime.datetime.now())
        )

    def testOnetoOneField(self):
        self.assertEqual(
            self.datafile.metadata,
            self.correctDataFileData["metadata"]
        )

    def testIncorrectData(self):
        with self.assertRaisesMessage(Exception, "NOT NULL constraint failed"):
            self.datafile = TestingDataFile.objects.create(
                title=self.incorrectDataFileData["title"],
                ancestorFile=self.correctDataFileData["ancestorFile"],
                metadata=self.correctDataFileData["metadata"]
            )
        with self.assertRaisesMessage(Exception, "You can't execute queries until the end of the 'atomic' block."):
            self.datafile = TestingDataFile.objects.create(
                title=self.correctDataFileData["title"],
                ancestorFile=self.incorrectDataFileData["ancestorFile"],
                metadata=self.correctDataFileData["metadata"]
            )
        with self.assertRaisesMessage(Exception, """must be a "TestingMetadataModel"""):
            self.datafile = TestingDataFile.objects.create(
                title=self.correctDataFileData["title"],
                ancestorFile=self.correctDataFileData["ancestorFile"],
                metadata=self.incorrectDataFileData["metadata"]
            )
