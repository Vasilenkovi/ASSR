from django.test import SimpleTestCase
from table_operations import TableFieldOpCSV
from StubDataFile import StubDataFile


class TableFieldOpCSVTest(SimpleTestCase):

    def setUp(self) -> None:
        self.csv_1 = StubDataFile("csv_1.csv")
        self.csv_2 = StubDataFile("csv_2.csv")
        self.pdf_1 = StubDataFile("pdf_1.pdf")

        return super().setUp()

    def test_zero_files(self):
        field_op_object = TableFieldOpCSV([])
        field_op_object.drop_columns([0, 1, 2])
        pass

    def test_single_file(self):
        field_op_object = TableFieldOpCSV([self.csv_1])
        field_op_object.drop_columns([0])
        pass
        
    def test_multiple_files(self):
        field_op_object = TableFieldOpCSV([self.csv_1, self.csv_2])
        field_op_object.drop_columns([2])
        pass

    def test_different_files(self):
        field_op_object = TableFieldOpCSV([self.csv_1, self.pdf_1])
        field_op_object.drop_columns([2])
        pass