from django.test import SimpleTestCase
from UploadSource.file_checker import FileChecker
from . import FILE_DIR_PATH


class TestFileChecker(SimpleTestCase):

    def setUp(self):
        self.file_csv = open(FILE_DIR_PATH / "csv.csv", "rb")
        self.file_pdf = open(FILE_DIR_PATH / "pdf.pdf", "rb")
        self.file_docx = open(FILE_DIR_PATH / "docx.docx", "rb")

        return super().setUp()
    
    def test_csv(self):
        checker = FileChecker(self.file_csv)
        self.assertTrue(checker.check_csv())

    def test_pdf(self):
        checker = FileChecker(self.file_pdf)
        self.assertTrue(checker.check_pdf())

    def test_check(self):
        checker = FileChecker(self.file_docx)
        self.assertFalse(checker.check())
