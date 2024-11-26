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
ROWS_OPERATION = 1
COLS_OPERATION = 0


@require_POST
def edit_cell(request, dataset_slug):
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    row = request.POST['row']
    column = request.POST['column']
    new_value = request.POST['new_value']
    location = json.loads(
        f'{{row: {row}, column: {column}}}'
    )
    data = json.loads(
        f'{{new_data: {new_value}}}'
    )
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
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    row = request.POST['row']
    location = json.loads(
        f'{{row: {row}}}'
    )
    transaction = transaction_handler(
        transaction_type=ROWS_OPERATION,
        location=location,
        transaction_direction=TRANSACTION_DELETE,
        description="Row delete",
    )
    _apply_transaction(transaction, dataset)


@require_POST
def remove_column(request, dataset_slug):
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    column = request.POST['column']
    location = json.loads(
        f'{{column: {column}}}'
    )
    transaction = transaction_handler(
        transaction_type=COLS_OPERATION,
        location=location,
        transaction_direction=TRANSACTION_DELETE,
        description="Column delete",
    )
    _apply_transaction(transaction, dataset)


@require_POST
def import_from(request, dataset_slug):
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    import_dataset = DatasetFile.objects.filter(metadata__pk=request.POST.import_dataset).get()
    imported_row_number = request.POST['row']
    imported_row = _get_row_from(import_dataset, imported_row_number)
    location = json.loads(
        f'{{row: NewLine}}'
    )
    data = json.loads(
        f'{{new_data: {imported_row}}}'
    )
    transaction = transaction_handler(
        transaction_type=ROWS_OPERATION,
        location=location,
        data=data,
        transaction_direction=TRANSACTION_EDIT_CREATE,
        description=f'Import from dataset {import_dataset.name}',
    )
    _apply_transaction(transaction, dataset)


@require_POST
def new_line(request, dataset_slug):
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    new_value = request.POST['new_value']
    location = json.loads(
        f'{{row: NewLine}}'
    )
    data = json.loads(
        f'{{new_data: {new_value}}}'
    )
    transaction = transaction_handler(
        transaction_type=ROWS_OPERATION,
        location=location,
        data=data,
        transaction_direction=TRANSACTION_EDIT_CREATE,
        description=f'New line',
    )
    _apply_transaction(transaction, dataset)
