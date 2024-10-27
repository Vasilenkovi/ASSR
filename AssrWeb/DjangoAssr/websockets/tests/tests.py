from DjangoAssr.websockets.consumer import AbstractConsumer
from django.test import SimpleTestCase


class AbstractConsumerTest(SimpleTestCase):

    def setUp(self):
        self.consumer = AbstractConsumer()

    def testRequestTypeTest(self):
        #incorrectData =  { "Type" : "DropRequest", "Columns" : [ col_id1, col_id2, ... col_idn], fileList: ["filename1", ... , "filename2]" }
        with self.assertRaisesMessage(Exception, "'AbstractConsumer' object has no attribute 'base_send'"):
            self.consumer.receive(text_data="""
            { "Type" : "Nonsense", "Columns" : "[ 0, 1, 2]", "fileList" : ["filename1", "filename2"]}""")
            self.consumer.receive(text_data="""
                        { "Type" : "DropRequest", "Columns" : "[ 0, 1, 2]", "fileList" : ["filename1", "filename2"]}""")
            self.consumer.receive(text_data="""
                                    { "Type" : "DropRequest", "Columns" : "[ 0, 1, 2]", "fileList" : [23, "filename2"]}""")
            self.consumer.receive(text_data="""
                                    { "Type" : "DropRequest", "AntiColumns" : "[ 0, 1, 2]", "fileList" : ["filename1", "filename2"]}""")
            self.consumer.receive(text_data="""
                                    { "AntyType" : "DropRequest", "Columns" : "[ 0, 1, 2]", "fileList" : ["filename1", "filename2"]}""")
            self.consumer.receive(text_data="""
                                    { "Type" : "DropRequest", "Columns" : "[ 0, 1, 2]", "AntyfileList" : ["filename1", "filename2"]}""")
            self.consumer.receive(text_data="""
                                    { "Type" : "DropRequest", "AntiColumns" : "[ 0, 1, 2]", "fileList" : ["filename1", "filename2"]}""")



