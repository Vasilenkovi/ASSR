from CreateDatasetApp.table_creator import TableCreator
from UploadSource.models import SourceFile
from CreateDatasetApp.models.transaction import Transaction


def _create_table(pk_list: list[int]) -> TableCreator:
    file_objs = SourceFile.objects.filter(
        pk__in=pk_list
    ).values("ancestorFile")
    file_bytes = [file["ancestorFile"] for file in file_objs]
    return TableCreator(file_bytes)


def transaction_handler(transaction_type: int, location: str, transaction_direction: int,
                        data: str | None = None, description: str | None = None, ) -> Transaction:
    """
    Returns Transaction object,
    :param data: data in location (for change and addition), null if deletion
    :param location: location of changed cell, rows or lines
    :param transaction_direction: 0 to change, 1 to remove
    :param transaction_type: 0 - operation on row(s), 1 - on coll(s), 2 - cell
    :param description:
    :return: Transaction object,need to be saved
    """
    transaction = Transaction.objects.create(
        description=description,
        location=location,
        transaction_direction=transaction_direction,
        transaction_type=transaction_type,
        data=data,
    )
    return transaction
