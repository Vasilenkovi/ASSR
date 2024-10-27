import datetime
import json
from django.test import TestCase
from MetaCommon.models.test_models import (TestingTagsModel, 
    TestingMetadataModel)


class MetadataTest(TestCase):

    def setUp(self):
        self.correctData = {"name": "BasedDataset Name15!", "author": "BasedCreator Name15!",
                             'keyValue': {"key1": "value1", "key2": "value2" },'keyValueJSON' : """ {"key1": "value1", "key2": "value2" } """,
                            "tags":["tag1", "tag2", "tag3"]}
        self.incorrectData = {"name": None, "author": None, 'keyValue': list(),
                            "tags":["tag1", "tag2", "tag3"]}

        self.metadataDict = TestingMetadataModel.objects.create(name=self.correctData["name"], author=self.correctData["author"],
                                             keyValue=self.correctData["keyValue"])
        self.metadataJSON = TestingMetadataModel.objects.create(name=self.correctData["name"], author=self.correctData["author"],
                                             keyValue=json.loads(self.correctData["keyValueJSON"]))
        for t in self.correctData["tags"]:
            tag = TestingTagsModel.objects.create(name=t)
            self.metadataDict.tag.add(tag)
            self.metadataJSON.tag.add(tag)
    def testDataTypes(self):
        self.propertiesJSON = [self.metadataJSON.name, self.metadataJSON.author, self.metadataJSON.creationData,
                               self.metadataJSON.keyValue, self.metadataJSON.tag]
        self.propertiesDict = [self.metadataDict.name, self.metadataDict.author, self.metadataDict.creationData,
                               self.metadataDict.keyValue, self.metadataDict.tag]

        for propertyID in range(len(self.propertiesDict)):
            self.assertEqual(type(self.propertiesJSON[propertyID]), type(self.propertiesDict[propertyID]))

        self.assertEqual(type(self.propertiesJSON[0]), str)
        self.assertEqual(type(self.propertiesJSON[1]), str)
        self.assertEqual(type(self.propertiesJSON[2]), datetime.datetime)
        self.assertEqual(type(self.propertiesJSON[3]), dict)
        for tag in self.propertiesJSON[4].all():
            self.assertEqual(type(tag.name), str)
            self.assertEqual(type(tag), TestingTagsModel)

        self.assertEqual(type(self.propertiesDict[0]), str)
        self.assertEqual(type(self.propertiesDict[1]), str)
        self.assertEqual(type(self.propertiesDict[2]), datetime.datetime)
        self.assertEqual(type(self.propertiesDict[3]), dict)
        for tag in self.propertiesDict[4].all():
            self.assertEqual(type(tag.name), str)
            self.assertEqual(type(tag), TestingTagsModel)
    def testManyToMany(self):
        allTags = [i.name for i in TestingTagsModel.objects.all()]
        for i in self.correctData['tags']:
            self.assertEqual(i in allTags, True)
        self.assertEqual(len(self.correctData['tags']), len(allTags))
    def testIncorrectData(self): #TODO change error messages
        with self.assertRaisesMessage(Exception, "NOT NULL constraint failed: MetaCommon_testingmetadatamodel.name"):
            self.metadata = TestingMetadataModel.objects.create(name=self.incorrectData["name"],
                                                                    author=self.correctData["author"],
                                                                    keyValue=self.correctData["keyValue"])
        with self.assertRaisesMessage(Exception, "An error occurred in the current transaction. You can't execute queries until the end of the 'atomic' block"):
            self.metadata = TestingMetadataModel.objects.create(name=self.correctData["name"],
                                                                    author=self.incorrectData["author"],
                                                                    keyValue=self.correctData["keyValue"])
        with self.assertRaisesMessage(Exception, "An error occurred in the current transaction. You can't execute queries until the end of the 'atomic' block."):
            self.metadata = TestingMetadataModel.objects.create(name=self.correctData["name"],
                                                                    author=self.correctData["author"],
                                                                    keyValue=self.incorrectData["keyValue"])

