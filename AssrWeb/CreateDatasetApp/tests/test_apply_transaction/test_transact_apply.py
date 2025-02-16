import pandas as pd
from io import BytesIO
import json
from django.test import TestCase
from CreateDatasetApp.views.utils import _apply_transaction, _get_row_from
from CreateDatasetApp.models.transaction import Transaction
from CreateDatasetApp.models import DatasetFile
from UploadSource.models import SourceFile
from CreateDatasetApp.models.transaction import TransactionType, TransactionDirection


class ApplyTransactionTestCase(TestCase):
    def setUp(self):
        self.initial_data = pd.DataFrame({
            "Name": ["Alice", "Bob", "Charlie"],
            "Age": [25, 30, 35],
            "City": ["New York", "Los Angeles", "Chicago"]
        })

        csv_bytes = BytesIO()
        self.initial_data.to_csv(csv_bytes, index=False)
        csv_bytes.seek(0)


        self.dataset = DatasetFile.objects.create(
            currentFile=csv_bytes.read()
        )


        self.source1 = SourceFile.objects.create(ancestorFile=b"BAZI_TEST1")
        self.source2 = SourceFile.objects.create(ancestorFile=b"BAZI_TEST2")

    def test_apply_transaction_add_row(self):
        new_row_data = {"Name": "Yarik", "Age": 1984, "City": "Bazistan"}
        transaction = Transaction.objects.create(
            transaction_type=TransactionType.ROWS,
            transaction_direction=TransactionDirection.CHANGE,
            location=json.dumps({"row": "NewLine"}),
            data=json.dumps({"new_data": new_row_data}),
            dataset=self.dataset
        )

        _apply_transaction(transaction, self.dataset)

        updated_df = pd.read_csv(BytesIO(self.dataset.currentFile))
        self.assertEqual(len(updated_df), len(self.initial_data) + 1)
        self.assertDictEqual(updated_df.iloc[-1].to_dict(), new_row_data)

    def test_apply_transaction_remove_row(self):
        transaction = Transaction.objects.create(
            transaction_type=TransactionType.ROWS,
            transaction_direction=TransactionDirection.REMOVE,
            location=json.dumps({"row": 1}),
            dataset=self.dataset
        )

        _apply_transaction(transaction, self.dataset)

        updated_df = pd.read_csv(BytesIO(self.dataset.currentFile))
        self.assertEqual(len(updated_df), len(self.initial_data) - 1)
        self.assertFalse((updated_df["Name"] == "Arthur BaziBazi").any())

    def test_apply_transaction_update_cell(self):
        new_value = "BaziBazi"
        transaction = Transaction.objects.create(
            transaction_type=TransactionType.CELL,
            transaction_direction=TransactionDirection.CHANGE,
            location=json.dumps({"row": 0, "column": 2}),
            data=json.dumps({"new_data": new_value}),
            dataset=self.dataset
        )

        _apply_transaction(transaction, self.dataset)

        updated_df = pd.read_csv(BytesIO(self.dataset.currentFile))
        self.assertEqual(updated_df.iat[0, 2], new_value)

    def test_apply_transaction_remove_column(self):
        transaction = Transaction.objects.create(
            transaction_type=TransactionType.COLS,
            transaction_direction=TransactionDirection.REMOVE,
            location=json.dumps({"column": 1}),
            dataset=self.dataset
        )

        _apply_transaction(transaction, self.dataset)

        updated_df = pd.read_csv(BytesIO(self.dataset.currentFile))
        self.assertNotIn("Age", updated_df.columns)

    def test_apply_transaction_add_source(self):
        transaction = Transaction.objects.create(
            transaction_type=TransactionType.SOURCE,
            transaction_direction=TransactionDirection.CHANGE,
            location=json.dumps({"location": "HEAD"}),
            data=json.dumps({"new_data": self.source1.pk}),
            dataset=self.dataset
        )

        _apply_transaction(transaction, self.dataset)

        self.assertIn(self.source1, self.dataset.source_list.all())

    def test_apply_transaction_remove_source(self):

        self.dataset.source_list.add(self.source2)

        transaction = Transaction.objects.create(
            transaction_type=TransactionType.SOURCE,
            transaction_direction=TransactionDirection.REMOVE,
            location=json.dumps({"location": "generic"}),
            data=json.dumps({"delete_source": self.source2.pk}),
            dataset=self.dataset
        )

        _apply_transaction(transaction, self.dataset)


        self.assertNotIn(self.source2, self.dataset.source_list.all())