from django.test import TestCase
from django.db import IntegrityError
from CreateDatasetApp.models import Transaction


class TestsTransaction(TestCase):

    def test_blank_type(self):
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                transaction_type=None,
                transaction_direction=0,
                location={"row": 0}
            )
    
    def test_blank_direction(self):
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                transaction_type=0,
                transaction_direction=None,
                location={"row": 0}
            )
    
    def test_blank_location(self):
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                transaction_type=0,
                transaction_direction=0,
                location=None
            )

    def test_oob_direction(self):
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                transaction_type=0,
                transaction_direction=10,
                location={"row": 0}
            )

    def test_oob_type(self):
        with self.assertRaises(IntegrityError):
            Transaction.objects.create(
                transaction_type=10,
                transaction_direction=0,
                location={"row": 0}
            )

    def test_save(self):
        Transaction.objects.create(
            description="transaction_1",
            transaction_type=1,
            transaction_direction=0,
            location={"row": 0},
            data=["aaa", "bbb", "ccc"]
        )