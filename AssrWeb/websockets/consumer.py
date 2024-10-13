import json
from channels.generic.websocket import WebsocketConsumer
import abc


class AbstractConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'message': 'Connection established'
        }))

    def disconnect(self, close_code):
        print("Socket connection lost")

    def receive(self, text_data=None, bytes_data=None):
        """
        Receives folowing types of JSON messages:

        1) DropRequest - request to drop collumns. Must follow the structure
        { "Type" : "DropRequest", "Columns" : [ col_id1, col_id2, ... col_idn], fileList: ["filename1", ... , "filename2]" }
        fileList - files related with drop requests, for example list of source-files if we work with source files,
        list with one item - name of dataset file during editing of dataset
        2) CreateTagRequest - request to create new tag. Must follow the structure
        { "Type" : "CreateTagRequest", "TagName" : "Text"}
        """
        message = json.loads(text_data)
        messageType = message["Type"]
        try:
            if messageType == "DropRequest":
                try:
                    columnsList = message["Columns"]
                    fileList = message["fileList"]
                except Exception as e:
                    self.send(
                        text_data=json.dumps({
                            'type': 'error_message',
                            'error': "Error during parsing: " +str(e)
                        }
                        ))
                else:
                    self.handlerColumnsDrop(columnsList, fileList)
            elif messageType == "CreateTagRequest":
                try:
                    tagName = message["TagName"]
                except Exception as e:
                    self.send(
                        text_data=json.dumps({
                            'type': 'error_message',
                            'error': "Error during parsing: " + str(e)
                        }
                        ))
                else:
                    self.handlerColumnsDrop(tagName) #Maybe cathinhg errors in handlers
                    # and sending notifications about them to frontend can be useful?
            else:
                raise Exception("Wrong request type")

        except Exception as e:
            self.send(
                text_data=json.dumps({
                    'type': 'error_message',
                    'error': str(e)
                }
                ))

    @abc.abstractmethod
    def handlerTagAddition(self, tagName):
        pass

    """
        Should handle requests for addition of new tags
    """

    @abc.abstractmethod
    def handlerColumnsDrop(self, columnsList, fileList):
        pass

    """
        Should handle requests for drop of columns
    """
