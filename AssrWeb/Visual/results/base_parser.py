from abc import ABC, abstractmethod
from json import loads
from .base_sample import Base_Sample


class Base_Parser(ABC):
    "Common interface to parse processing JSONs into sample instances"

    sample_class = Base_Sample
    sample_list: list[Base_Sample]

    def __init__(self, processing_json: str | dict):
        "Accepts result JSON as a dict or as a JSON string that encodes dict"

        parse_source = processing_json
        if isinstance(parse_source, str):
            parse_source = loads(parse_source)

        if not isinstance(parse_source, dict):
            raise AttributeError("processing_json can not be cast to a dict")

        self.sample_list = self.parse_json(parse_source)
        super().__init__()

    def get_implemented_sample_methods(self) -> tuple:
        return self.sample_class.get_implemetned_methods()

    @abstractmethod
    def parse_json(self, in_json: dict) -> list[Base_Sample]:
        pass
