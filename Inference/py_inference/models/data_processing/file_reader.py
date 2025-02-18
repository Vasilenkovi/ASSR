from enum import Enum
from io import BytesIO
from typing import Generator
from nltk import tokenize, download
from pandas import read_csv
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from .converters import Base_Converter, CSV_Converter, PDF_Converter


class File_reader:

    class File_Type(Enum):
        PDF = 0
        CSV = 1

    binary_file: bytes
    column_ids: None | list[int]
    file_type: File_Type

    def __init__(self, in_file: bytes, in_column_ids: None | list[int]):
        """in_column_ids is used when csv files are processed 
        to only condiser selected columns"""

        self.binary_file = in_file
        self.column_ids = in_column_ids

        valid_file = False

        try:
            PdfReader(BytesIO(self.binary_file))
            valid_file = True
            self.file_type = File_reader.File_Type.PDF
        except PdfReadError:
            pass

        try:
            read_csv(BytesIO(self.binary_file))
            valid_file = True
            self.file_type = File_reader.File_Type.CSV
        except UnicodeDecodeError:
            pass

        if not valid_file:
            raise AttributeError("Not a valid csv or pdf file")

        download('punkt_tab')

    def get_sample(self) -> Generator[Base_Converter]:

        if self.file_type == File_reader.File_Type.PDF:
            return self.get_sample_pdf()
        elif self.file_type == File_reader.File_Type.CSV:
            return self.get_sample_csv()
        
        raise NotImplementedError("File type is not supported")

    def get_sample_pdf(self) -> Generator[PDF_Converter]:
        reader = PdfReader(BytesIO(self.binary_file))
        page_text = [p.extract_text() for p in reader.pages]
        file_string = " ".join(page_text)

        for i, sentence in enumerate(tokenize.sent_tokenize(file_string)):
            yield PDF_Converter(sentence, i)

    def get_sample_csv(self) -> Generator[CSV_Converter]:
        df = read_csv(BytesIO(self.binary_file))
        
        if self.column_ids:
            df = df.iloc[:, self.column_ids]

        for row_id, row in df.iterrows():
            for column_id, cell in row.items():
                for i, sentence in enumerate(tokenize.sent_tokenize(cell)):
                    yield CSV_Converter(sentence, row_id, column_id, i)
