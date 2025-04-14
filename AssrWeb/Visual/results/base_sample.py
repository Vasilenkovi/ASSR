from abc import ABC, abstractmethod


class Base_Sample(ABC):
    "Common interface of a datapoint object"

    sentence_id: int
    monotonous_id: int
    sample_object: dict

    def __init__(
        self,
        in_sample_object: dict,
        in_monotonous_id: int
    ):
        self.sentence_id = in_sample_object.get("sentence")
        self.monotonous_id = in_monotonous_id
        self.sample_object = in_sample_object

    @staticmethod
    @abstractmethod
    def get_implemented_methods() -> tuple:
        """Produces a tuple with implemented method names"""

    @abstractmethod
    def get_similarity(self, rhs: "Base_Sample") -> float:
        """Produces a scalar metric of similarity between samples"""

    @abstractmethod
    def get_values(self) -> list[float]:
        """Produces a vector of numerical characteristics of a sample"""

    def get_input_text(self) -> str | None:
        return self.sample_object.get("input")
