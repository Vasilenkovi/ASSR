from abc import ABC, abstractmethod


class Base_Converter(ABC):
    """Common interface to generate JSON dict entries that incapsulate 
    information about which data was processed by model"""

    input_str: str

    @abstractmethod
    def save(output: dict) -> dict:
        pass


class CSV_Converter(Base_Converter):

    row_num: int
    column_num: int
    sentence_num: int

    def __init__(
            self, in_input_str: str, in_row: int,
            in_column: int, in_sentence: int
        ):

        self.input_str = in_input_str
        self.row_num = in_row
        self.column_num = in_column
        self.sentence_num = in_sentence

        super().__init__()

    def save(self, output: dict) -> dict:
        return {
            "row": self.row_num,
            "column": self.column_num,
            "sentence": self.sentence_num,
            "input": self.input_str,
            "output": output
        }


class PDF_Converter(Base_Converter):

    sentence_num: int

    def __init__(self, in_input_str: str, in_sentence: int):

        self.input_str = in_input_str
        self.sentence_num = in_sentence

        super().__init__()

    def save(self, output: dict) -> dict:
        return {
            "sentence": self.sentence_num,
            "input": self.input_str,
            "output": output
        }
