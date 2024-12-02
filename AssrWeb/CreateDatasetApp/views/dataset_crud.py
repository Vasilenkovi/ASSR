import json
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from .utils import _apply_transaction, transaction_handler, _get_row_from


@require_POST
def delete_dataset(request, dataset_slug):
    DatasetFile.objects.filter(metadata__pk=dataset_slug).get().delete()
    DatasetMetadata.objects.filter(pk=dataset_slug).get().delete()
    return redirect('dataset:datasets-list')


TRANSACTION_EDIT_CREATE = 0
TRANSACTION_DELETE = 1
CELL_OPERATION = 2
ROWS_OPERATION = 0
COLS_OPERATION = 1


@require_POST
def edit_cell(request, dataset_slug):
    """
    :param request: requires parameters:
    row - index of row
    column - index of column
    new_data - new content of cell
    :param dataset_slug:
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    row = request.POST.get('row')
    column = request.POST.get('column')
    new_value = request.POST.get('new_value')
    location = json.dumps({"row": row, "column": column})
    data = json.dumps({"new_data": new_value})
    transaction = transaction_handler(
        transaction_type=CELL_OPERATION,
        location=location,
        transaction_direction=TRANSACTION_EDIT_CREATE,
        data=data,
        description="Cell update",
    )
    _apply_transaction(transaction, dataset)


@require_POST
def remove_row(request, dataset_slug):
    """
    :param request: requires parameters:
    row - index of row to delete
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    row = request.POST.get('row')
    location = json.dumps({"row": row})
    transaction = transaction_handler(
        transaction_type=ROWS_OPERATION,
        location=location,
        transaction_direction=TRANSACTION_DELETE,
        description="Row delete",
    )
    _apply_transaction(transaction, dataset)


@require_POST
def remove_column(request, dataset_slug):
    """
    :param request: requires parameters:
    column - index of column to delete
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    column = request.POST.get('column')
    location = json.dumps({"column": column})
    transaction = transaction_handler(
        transaction_type=COLS_OPERATION,
        location=location,
        transaction_direction=TRANSACTION_DELETE,
        description="Column delete",
    )
    _apply_transaction(transaction, dataset)


@require_POST
def import_from(request, dataset_slug):
    """
    :param request: requires parameters:
    import_dataset - index of dataset to import row from him
    imported_row - index of row in import_dataset
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    import_dataset = DatasetFile.objects.filter(metadata__pk=request.POST.get('import_dataset')).get()
    imported_row_number = request.POST.get('imported_row')
    imported_row = _get_row_from(import_dataset, imported_row_number)
    location = json.dumps({"row": "NewLine"})
    data = json.dumps({"new_data": imported_row})
    transaction = transaction_handler(
        transaction_type=ROWS_OPERATION,
        location=location,
        data=data,
        transaction_direction=TRANSACTION_EDIT_CREATE,
        description=f'Import from dataset {import_dataset.metadata.name}',
    )
    _apply_transaction(transaction, dataset)


@require_POST
def new_line(request, dataset_slug):
    """
    :param request:
    new_value - json with new line example {"Name": "Bazi", "Age": 666, "City": 78812}
    :param dataset_slug:
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    new_value = request.POST.get('new_value')
    location = json.dumps({"row": "NewLine"})
    data = json.dumps({"new_data": json.loads(new_value)})
    transaction = transaction_handler(
        transaction_type=ROWS_OPERATION,
        location=location,
        data=data,
        transaction_direction=TRANSACTION_EDIT_CREATE,
        description=f'New line',
    )
    _apply_transaction(transaction, dataset)
