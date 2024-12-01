import pandas as pd
import json
from io import BytesIO
from CreateDatasetApp.table_creator import TableCreator
from UploadSource.models import SourceFile
from CreateDatasetApp.models.transaction import Transaction
from CreateDatasetApp.models import DatasetFile


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
    :param transaction_direction: 0 to change or add, 1 to remove
    :param transaction_type: 0 - operation on row(s), 1 - on coll(s), 2 - cell
    :param description: wow it is description!
    :return: Transaction object,need to be saved
    """
    transaction = Transaction(
        description=description,
        location=location,
        transaction_direction=transaction_direction,
        transaction_type=transaction_type,
        data=data,
    )
    return transaction


def _apply_transaction(transaction: Transaction, dataset: DatasetFile) -> None:
    dataset_pd = pd.read_csv(BytesIO(dataset.currentFile), index_col=None)
    location = json.loads(transaction.location)
    if transaction.transaction_direction == 0:
        new_data = json.loads(transaction.data)
        new_data = new_data['new_data']
        if transaction.transaction_type == 0:
            if location['row'] != 'NewLine':
                dataset_pd.loc[location['row']] = new_data
            else:
                dataset_pd.loc[len(dataset_pd)] = new_data
        if transaction.transaction_type == 1:
            dataset_pd.iloc[:, location['column']] = new_data
        if transaction.transaction_type == 2:
            dataset_pd.iat[int(location['row']), int(location['column'])] = new_data
    elif transaction.transaction_direction == 1:
        if transaction.transaction_type == 0:
            dataset_pd = dataset_pd.drop(index=int(location['row']))
        if transaction.transaction_type == 1:
            dataset_pd = dataset_pd.drop(dataset_pd.columns[int(location['column'])], axis=1)
    csv_bytes = BytesIO()
    dataset_pd.to_csv(csv_bytes, index=False)
    csv_bytes.seek(0)
    dataset.currentFile = csv_bytes.read()
    dataset.save()
    transaction.dataset = dataset
    transaction.save()


def _get_row_from(dataset: DatasetFile, row_number: str) -> dict:
    dataset_pd = pd.read_csv(BytesIO(dataset.currentFile))
    row_data = dataset_pd.iloc[int(row_number)]
    row_json = row_data.to_json()
    return row_json
