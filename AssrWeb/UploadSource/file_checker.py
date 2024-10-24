from io import BytesIO
from pandas import read_csv
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError


class FileChecker:

    def __init__(self, file: BytesIO):
        self.file = file

    def check_pdf(self) -> bool:
        try:
            PdfReader(self.file)
            return True
        
        except PdfReadError:
            return False
        
    def check_csv(self) -> bool:
        try:
            read_csv(self.file)
            return True
        
        except UnicodeDecodeError:
            return False
    
    def check(self) -> bool:
        return self.check_pdf() or self.check_csv()