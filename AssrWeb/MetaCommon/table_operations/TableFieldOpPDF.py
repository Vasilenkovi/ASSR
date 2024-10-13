from .TableFieldOp import TableFieldOp
from .FileMismatchException import FileMismatchException
from pandas import DataFrame
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


class TableFieldOpPDF(TableFieldOp):

    def _coerce_to_table(self, file_list: list["DataFile"]) -> DataFrame:
        if len(file_list) == 0:
            return DataFrame()

        records = []
        for pdf in file_list:

            reader = None
            try:
                reader = PdfReader(pdf.file)
            except PdfReadError:
                raise FileMismatchException("Expected PDF file, found other")

            page_test = [p.extract_text() for p in reader.pages]
            records.append(" \n ".join(page_test))

        return DataFrame(records, columns=["documents"])