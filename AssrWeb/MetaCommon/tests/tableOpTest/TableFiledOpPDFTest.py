from django.test import SimpleTestCase
from table_operations import TableFieldOpPDF
from StubDataFile import StubDataFile


class TableFieldOpCSVTest(SimpleTestCase):

    def setUp(self) -> None:
        self.pdf_1 = StubDataFile("pdf_1.pdf")
        self.pdf_2 = StubDataFile("pdf_2.pdf")
        self.csv_1 = StubDataFile("csv_1.csv")

        return super().setUp()

    def test_zero_files(self):
        field_op_object = TableFieldOpPDF([])
        pass

    def test_single_file(self):
        field_op_object = TableFieldOpPDF([self.pdf_1])
        pass
        
    def test_multiple_files(self):
        field_op_object = TableFieldOpPDF([self.pdf_1, self.pdf_2])
        pass

    def test_different_files(self):
        field_op_object = TableFieldOpPDF([self.csv_1, self.pdf_1])
        pass

    def test_drop_only_column(self):
        field_op_object = TableFieldOpPDF([self.pdf_1])
        field_op_object.drop_columns([0])
        pass

    def test_drop_out_of_range(self):
        field_op_object = TableFieldOpPDF([self.pdf_1])
        field_op_object.drop_columns([1])
        pass