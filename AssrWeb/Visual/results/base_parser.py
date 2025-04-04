from abc import ABC, abstractmethod
from .base_sample import Base_Sample


class Base_Parser(ABC):
    "Common interface to parse processing JSONs into sample instances"

    sample_class = Base_Sample
    sample_list: list[Base_Sample]

    def __init__(self, processing_json: str):
        self.sample_list = self.parse_json(processing_json)
        super().__init__()

    def get_implemented_sample_methods(self) -> dict:
        return self.sample_class.get_implemetned_methods()

    @abstractmethod
    def parse_json(self, in_json: str) -> list[Base_Sample]:
        pass
