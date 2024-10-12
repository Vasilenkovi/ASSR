from django.test import SimpleTestCase
from MetaCommon.table_operations.TableFieldOpPDF import TableFieldOpPDF
from MetaCommon.table_operations.FileMismatchException import FileMismatchException
from MetaCommon.table_operations.IndexListOOBException import IndexListOOBException
from .StubDataFile import StubDataFile
from . import FILE_DIR_PATH


class TableFieldOpPDFTest(SimpleTestCase):

    def setUp(self) -> None:
        self.pdf_1 = StubDataFile(FILE_DIR_PATH / "pdf_1.pdf")
        self.pdf_2 = StubDataFile(FILE_DIR_PATH / "pdf_2.pdf")
        self.csv_1 = StubDataFile(FILE_DIR_PATH / "csv_1.csv")

        return super().setUp()

    def test_zero_files(self):
        field_op_object = TableFieldOpPDF([])
        self.assertTrue(
            field_op_object.table.empty
        )

    def test_single_file(self):
        field_op_object = TableFieldOpPDF([self.pdf_1])
        self.assertEqual(
            field_op_object.table.to_numpy().shape,
            (1, 1)
        )
        self.assertEqual(
            field_op_object.table.columns[0],
            "documents"
        )

    def test_multiple_files(self):
        field_op_object = TableFieldOpPDF([self.pdf_1, self.pdf_2])
        self.assertEqual(
            field_op_object.table.to_numpy().shape,
            (2, 1)
        )
        self.assertEqual(
            field_op_object.table.columns[0],
            "documents"
        )

    def test_different_files(self):
        with self.assertRaises(FileMismatchException):
            TableFieldOpPDF([self.csv_1, self.pdf_1])

    def test_drop_only_column(self):
        field_op_object = TableFieldOpPDF([self.pdf_1])
        field_op_object.drop_columns([0])
        self.assertTrue(
            field_op_object.table.empty
        )

    def test_drop_out_of_range(self):
        field_op_object = TableFieldOpPDF([self.pdf_1])
        with self.assertRaises(IndexListOOBException):
            field_op_object.drop_columns([1])
