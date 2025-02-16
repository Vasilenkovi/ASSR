import json
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from CreateDatasetApp.models.transaction import TransactionType, TransactionDirection
from .utils import _apply_transaction, transaction_handler, _get_row_from


@require_POST
def delete_dataset(request, dataset_slug):
    DatasetFile.objects.filter(metadata__pk=dataset_slug).get().delete()
    DatasetMetadata.objects.filter(pk=dataset_slug).get().delete()
    return redirect('dataset:datasets-list')






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
        transaction_type=TransactionType.CELL,
        location=location,
        transaction_direction=TransactionDirection.CHANGE,
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
        transaction_type=TransactionType.ROWS,
        location=location,
        transaction_direction=TransactionDirection.REMOVE,
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
        transaction_type=TransactionType.COLS,
        location=location,
        transaction_direction=TransactionDirection.REMOVE,
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
        transaction_type=TransactionType.ROWS,
        location=location,
        data=data,
        transaction_direction=TransactionDirection.CHANGE,
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
        transaction_type=TransactionType.ROWS,
        location=location,
        data=data,
        transaction_direction=TransactionDirection.CHANGE,
        description=f'New line',
    )
    _apply_transaction(transaction, dataset)


@require_POST
def new_source(request):
    """
    :param request:
    new_value - json with new line example {"dataset_slug": "slug", "source_file_slug": "slug", "position": "TAIL/HEAD"}
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=request.POST.get('dataset_slug')).get()
    source_file_slug = request.POST.get('source_file_slug')
    position = request.POST.get("position")
    location = json.dumps({"location": position})
    data = json.dumps({"new_data": source_file_slug})
    transaction = transaction_handler(
        transaction_type=TransactionType.SOURCE,
        location=location,
        data=data,
        transaction_direction=TransactionDirection.CHANGE,
        description=f'New source',
    )
    _apply_transaction(transaction, dataset)



@require_POST
def delete_source(request):
    """
    :param request:
    new_value - json with new line example {"dataset_slug": "slug", "source_file_pk": pk}
    :return:
    """
    dataset = DatasetFile.objects.filter(metadata__pk=request.POST.get('dataset_slug')).get()
    source_file_slug = request.POST.get('source_file_slug')
    position = "generic"
    location = json.dumps({"location": position})
    data = json.dumps({"delete_source": source_file_slug})
    transaction = transaction_handler(
        transaction_type=TransactionType.SOURCE,
        location=location,
        data=data,
        transaction_direction=TransactionDirection.REMOVE,
        description=f'Delete source',
    )
    _apply_transaction(transaction, dataset)


