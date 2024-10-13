from django.test import SimpleTestCase
from MetaCommon.table_operations.TableFieldOpCSV import TableFieldOpCSV
from MetaCommon.table_operations.FileMismatchException import FileMismatchException
from MetaCommon.table_operations.IndexListOOBException import IndexListOOBException
from .StubDataFile import StubDataFile
from . import FILE_DIR_PATH


class TableFieldOpCSVTest(SimpleTestCase):

    def setUp(self):
        self.csv_1 = StubDataFile(FILE_DIR_PATH / "csv_1.csv")
        self.csv_2 = StubDataFile(FILE_DIR_PATH / "csv_2.csv")
        self.pdf_1 = StubDataFile(FILE_DIR_PATH / "pdf_1.pdf")

        return super().setUp()

    def test_zero_files(self):
        field_op_object = TableFieldOpCSV([])

        with self.assertRaises(IndexListOOBException):
            field_op_object.drop_columns([0, 1, 2])

    def test_single_file(self):
        field_op_object = TableFieldOpCSV(
            [self.csv_1]
        )
        field_op_object.drop_columns([0])
        self.assertEqual(
            field_op_object.table.to_numpy().shape,
            (2, 2)
        )
        self.assertEqual(
            field_op_object.table.columns[0],
            "col 2"
        )
        self.assertEqual(
            field_op_object.table.columns[1],
            "col 3"
        )

    def test_multiple_files(self):
        field_op_object = TableFieldOpCSV(
            [self.csv_1, self.csv_2]
        )
        field_op_object.drop_columns([2])
        self.assertEqual(
            field_op_object.table.to_numpy().shape,
            (4, 2)
        )
        self.assertEqual(
            field_op_object.table.columns[0],
            "col 1"
        )
        self.assertEqual(
            field_op_object.table.columns[1],
            "col 2"
        )

    def test_different_files(self):
        with self.assertRaises(FileMismatchException):
            TableFieldOpCSV(
                [self.csv_1, self.pdf_1]
            )
