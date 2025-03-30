from csv import Sniffer, Error
from enum import Enum
from io import BytesIO
import logging
from typing import Generator, Optional
from nltk import tokenize, download
from pandas import read_csv
from pypdf import PdfReader
from pypdf.errors import PdfReadError
from .converters import Base_Converter, CSV_Converter, PDF_Converter


logger = logging.getLogger("pypdf") # Disregard logging for potentially malformed files
logger.setLevel(logging.CRITICAL)


class File_reader:

    MAX_CHARACTER_LENGTH = 512

    class File_Type(Enum):
        PDF = 0
        CSV = 1

    binary_file: bytes
    column_ids: Optional[list[int]]
    file_type: File_Type

    def __init__(self, in_file: bytes,
                 in_column_ids: Optional[list[int]] = None
        ):
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
            Sniffer().sniff(
                self.binary_file[:4096].decode() # Try to infer csv dialect from delimeters
            )
            read_csv(BytesIO(self.binary_file))
            valid_file = True
            self.file_type = File_reader.File_Type.CSV
        except Error: # Could not get csv dialect
            pass
        except UnicodeDecodeError: # Nonexistent unicode codepoints => not a plaintext csv
            pass

        if not valid_file:
            raise AttributeError("Not a valid csv or pdf file")

        download('punkt_tab', quiet=True)

    def get_sample(self) -> Generator[Base_Converter, None, None]:

        if self.file_type == File_reader.File_Type.PDF:
            return self.get_sample_pdf()
        elif self.file_type == File_reader.File_Type.CSV:
            return self.get_sample_csv()
        
        raise NotImplementedError("File type is not supported")

    def get_sample_pdf(self) -> Generator[PDF_Converter, None, None]:
        reader = PdfReader(BytesIO(self.binary_file))
        page_text = [p.extract_text() for p in reader.pages]
        file_string = " ".join(page_text)

        index = 0
        for sentence in tokenize.sent_tokenize(file_string):
            clean = File_reader._clean_sentence(sentence)
            chunks = File_reader._get_chunks(clean)
            for c in chunks:
                yield PDF_Converter(c, index)
                index += 1

    def get_sample_csv(self) -> Generator[CSV_Converter, None, None]:
        df = read_csv(BytesIO(self.binary_file))
        
        if self.column_ids:
            df = df.iloc[:, self.column_ids]

        for row_id, row in df.iterrows():
            for column_id, cell in row.items():
                index = 0
                for sentence in tokenize.sent_tokenize(cell):
                    clean = File_reader._clean_sentence(sentence)
                    chunks = File_reader._get_chunks(clean)
                    for c in chunks:
                        yield CSV_Converter(c, row_id, column_id, index)
                        index += 1

    @staticmethod
    def _clean_sentence(in_sentence: str) -> str:
        return in_sentence \
            .replace("\n", " ") \
            .strip()
    
    @staticmethod
    def _get_chunks(in_clean_sent: str) -> tuple[str]:
        return (
            in_clean_sent[offset:offset + File_reader.MAX_CHARACTER_LENGTH]
            for offset in range(
                0,
                len(in_clean_sent),
                File_reader.MAX_CHARACTER_LENGTH
            )
        )
