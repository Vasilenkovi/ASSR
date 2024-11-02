from django.test import SimpleTestCase
from numpy import isnan
from CreateDatasetApp.table_creator import TableCreator
from . import FILE_DIR_PATH


class TestTableCreator(SimpleTestCase):

    def setUp(self):
        self.csv_1 = open(FILE_DIR_PATH / "csv_1.csv", "rb").read()
        self.csv_2 = open(FILE_DIR_PATH / "csv_2.csv", "rb").read()
        self.csv_3 = open(FILE_DIR_PATH / "csv_3.csv", "rb").read()
        self.csv_single_1 = open(FILE_DIR_PATH / "csv_single_1.csv", "rb").read()
        self.csv_single_2 = open(FILE_DIR_PATH / "csv_single_2.csv", "rb").read()
        self.pdf_1 = open(FILE_DIR_PATH / "pdf_1.pdf", "rb").read()
        self.pdf_2 = open(FILE_DIR_PATH / "pdf_2.pdf", "rb").read()

        return super().setUp()

    def test_csv_union(self):
        tc = TableCreator([self.csv_1, self.csv_2])
        df = tc.to_dataframe()
        
        self.assertEqual(
            df.shape,
            (4, 3)
        )
        self.assertTrue(
            isnan(df.iloc[2, 2])
        )


    def test_csv_pure_intersection(self):
        tc = TableCreator([self.csv_2, self.csv_3])
        df = tc.to_dataframe()
        
        self.assertEqual(
            df.shape,
            (4, 2)
        )
        self.assertFalse(
            isnan(df.iloc[2, 1])
        )



    def test_pdf_collection(self):
        tc = TableCreator([self.pdf_1, self.pdf_2])
        df = tc.to_dataframe()
        
        self.assertEqual(
            df.shape,
            (2, 1)
        )


    def test_csv_pdf_single_column(self):
        tc = TableCreator([self.pdf_1, self.pdf_2, 
                           self.csv_single_1, self.csv_single_2])
        df = tc.to_dataframe()
        
        self.assertEqual(
            df.shape,
            (4, 1)
        )


    def test_csv_pdf_mix(self):
        tc = TableCreator([self.pdf_1, self.pdf_2, 
                           self.csv_1, self.csv_single_1])
        df = tc.to_dataframe()
        
        self.assertEqual(
            df.shape,
            (6, 4)
        )
        self.assertTrue(
            isnan(df.iloc[1, 1])
        )
        self.assertFalse(
            isnan(df.iloc[2, 2])
        )