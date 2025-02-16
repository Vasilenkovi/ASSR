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


def process_transaction(dataset_slug: str, location_value: dict | None, data_field: dict | None,
                        transaction_type: int, direction: int, description: str) -> None:
    dataset = DatasetFile.objects.filter(metadata__pk=dataset_slug).get()
    location = json.dumps(location_value)
    data = json.dumps(data_field) if data_field else None

    transaction = transaction_handler(
        transaction_type=transaction_type,
        location=location,
        data=data,
        transaction_direction=direction,
        description=description,
    )
    _apply_transaction(transaction, dataset)



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
    process_transaction(
        dataset_slug=dataset_slug,
        location_value={
            "row": request.POST.get('row'),
            "column": request.POST.get('column')
        },
        data_field={"new_data": request.POST.get('new_value')},
        transaction_type=TransactionType.CELL,
        direction=TransactionDirection.CHANGE,
        description="Cell update"
    )


@require_POST
def remove_row(request, dataset_slug):
    """
    :param request: requires parameters:
    row - index of row to delete
    :return:
    """
    process_transaction(
        dataset_slug=dataset_slug,
        location_value={"row": request.POST.get('row')},
        data_field=None,
        transaction_type=TransactionType.ROWS,
        direction=TransactionDirection.REMOVE,
        description="Row delete"
    )


@require_POST
def remove_column(request, dataset_slug):
    """
    :param request: requires parameters:
    column - index of column to delete
    :return:
    """
    process_transaction(
        dataset_slug=dataset_slug,
        location_value={"column": request.POST.get('column')},
        data_field=None,
        transaction_type=TransactionType.COLS,
        direction=TransactionDirection.REMOVE,
        description="Column delete"
    )
    return redirect('dataset:datasets-list')


@require_POST
def import_from(request, dataset_slug):
    """
    :param request: requires parameters:
    import_dataset - index of dataset to import row from him
    imported_row - index of row in import_dataset
    :return:
    """
    imported_row = json.loads(request.POST.get('imported_row'))
    process_transaction(
        dataset_slug=dataset_slug,
        location_value={"row": "NewLine"},
        data_field={"new_data": imported_row},
        transaction_type=TransactionType.ROWS,
        direction=TransactionDirection.CHANGE,
        description=f'Import from dataset {request.POST.get("import_dataset")}'
    )


@require_POST
def new_line(request, dataset_slug):
    """
    :param request:
    new_value - json with new line example {"Name": "Bazi", "Age": 666, "City": 78812}
    :param dataset_slug:
    :return:
    """
    process_transaction(
        dataset_slug=dataset_slug,
        location_value={"row": "NewLine"},
        data_field={"new_data": json.loads(request.POST.get('new_value'))},
        transaction_type=TransactionType.ROWS,
        direction=TransactionDirection.CHANGE,
        description='New line'
    )


@require_POST
def new_source(request):
    """
    :param request:
    new_value - json with new line example {"dataset_slug": "slug", "source_file_slug": "slug", "position": "TAIL/HEAD"}
    :return:
    """
    process_transaction(
        dataset_slug=request.POST.get('dataset_slug'),
        location_value=request.POST.get('position'),
        data_field={"new_data": request.POST.get('source_file_slug')},
        transaction_type=TransactionType.SOURCE,
        direction=TransactionDirection.CHANGE,
        description='New source'
    )



@require_POST
def delete_source(request):
    """
    :param request:
    new_value - json with new line example {"dataset_slug": "slug", "source_file_pk": pk}
    :return:
    """
    process_transaction(
        dataset_slug=request.POST.get('dataset_slug'),
        location_value=None,
        data_field={"delete_source": request.POST.get('source_file_slug')},
        transaction_type=TransactionType.SOURCE,
        direction=TransactionDirection.REMOVE,
        description='Delete source'
    )


