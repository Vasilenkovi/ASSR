from ProcessingApp.models import Processing_model
from ProcessingApp.views.results_display import fetch_processing_result
from .base_parser import Base_Parser
from .text import Text_Parser
from .token import Token_Parser


class Inference_Not_performed_Error(AttributeError):
    def __init__(self, in_pk: int, *args, name = ..., obj = ...):
        self.pk = in_pk
        super().__init__(*args, name=name, obj=obj)

    def __str__(self):
        return f"Processing record {self.pk} has no task set. No inference was performed"


class Task_Not_Supported_Error(AttributeError):
    def __init__(self, in_pk: int, in_task: int, *args, name = ..., obj = ...):
        self.pk = in_pk
        self.task = in_task
        super().__init__(*args, name=name, obj=obj)

    def __str__(self):
        return f"Task {self.task} on processing record {self.pk} is not supported"
    

class MongoDB_Proxy:

    def find_one(self, in_pk: int) -> dict:
        return fetch_processing_result(in_pk)[0]


def parser_factory(
    processing_obj: Processing_model,
    mongo_proxy = MongoDB_Proxy()
) -> Base_Parser:

    # If no processing was performed
    if processing_obj.task is None:
        raise Inference_Not_performed_Error(processing_obj.pk)
    
    match processing_obj.task:

        case Processing_model.Task.Text_class.value:
            json_result = mongo_proxy.find_one(processing_obj.pk)
            return Text_Parser(json_result)
        
        case Processing_model.Task.Token_class.value:
            json_result = mongo_proxy.find_one(processing_obj.pk)
            return Token_Parser(json_result)
        
        case _:
            raise Task_Not_Supported_Error(processing_obj.pk, processing_obj.task)
