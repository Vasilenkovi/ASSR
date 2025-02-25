import json
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from CreateDatasetApp.models.transaction import TransactionType, TransactionDirection
from .utils import _apply_transaction, transaction_handler, _get_row_from


@require_POST
def delete_dataset(request, dataset_slug):
    try:
        DatasetFile.objects.filter(metadata__pk=dataset_slug).get().delete()
        DatasetMetadata.objects.filter(pk=dataset_slug).get().delete()
        return redirect('dataset:datasets-list')
    except ObjectDoesNotExist:
        return HttpResponse(status=404)  # Not Found
    except Exception as e:
        return HttpResponse(status=500)  # Internal Server Error


def process_transaction(dataset_slug: str, location_value: dict | None, data_field: dict | None,
                        transaction_type: int, direction: int, description: str) -> None:
    try:
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
    except ObjectDoesNotExist:
        raise ValueError("Dataset not found")
    except Exception as e:
        raise RuntimeError(f"Transaction failed: {str(e)}")


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
    return HttpResponse(status=200)  # OK


@require_POST
def remove_row(request, dataset_slug):
    """
    :param request: requires parameters:
    row - index of row to delete
    :return:
    """
    try:
        process_transaction(
            dataset_slug=dataset_slug,
            location_value={"row": request.POST.get('row')},
            data_field=None,
            transaction_type=TransactionType.ROWS,
            direction=TransactionDirection.REMOVE,
            description="Row delete"
        )
        return HttpResponse(status=200)  # OK
    except ValueError:
        return HttpResponse(status=404)  # Not Found
    except RuntimeError:
        return HttpResponse(status=500)  # Internal Server Error

@require_POST
def remove_column(request, dataset_slug):
    """
    :param request: requires parameters:
    column - index of column to delete
    :return:
    """
    try:
        process_transaction(
            dataset_slug=dataset_slug,
            location_value={"column": request.POST.get('column')},
            data_field=None,
            transaction_type=TransactionType.COLS,
            direction=TransactionDirection.REMOVE,
            description="Column delete"
        )
        return HttpResponse(status=200)  # OK
    except ValueError:
        return HttpResponse(status=404)  # Not Found
    except RuntimeError:
        return HttpResponse(status=500)  # Internal Server Error


@require_POST
def import_from(request, dataset_slug):
    """
    :param request: requires parameters:
    import_dataset - index of dataset to import row from him
    imported_row - index of row in import_dataset
    :return:
    """
    imported_row = json.loads(request.POST.get('imported_row'))
    if not all(param in request.POST for param in required_params):
        return HttpResponse(status=400)  # Bad Request
    try:
        process_transaction(
            dataset_slug=dataset_slug,
            location_value={"row": "NewLine"},
            data_field={"new_data": imported_row},
            transaction_type=TransactionType.ROWS,
            direction=TransactionDirection.CHANGE,
            description=f'Import from dataset {request.POST.get("import_dataset")}'
        )
        return HttpResponse(status=201)  # Created
    except json.JSONDecodeError:
        return HttpResponse(status=400)  # Bad Request
    except ValueError:
        return HttpResponse(status=404)  # Not Found
    except RuntimeError:
        return HttpResponse(status=500)  # Internal Server Error

@require_POST
def new_line(request, dataset_slug):
    """
    :param request:
    new_value - json with new line example {"Name": "Bazi", "Age": 666, "City": 78812}
    :param dataset_slug:
    :return:
    """
    if 'new_value' not in request.POST:
        return HttpResponse(status=400)  # Bad Request

    try:
        process_transaction(
            dataset_slug=dataset_slug,
            location_value={"row": "NewLine"},
            data_field={"new_data": json.loads(request.POST.get('new_value'))},
            transaction_type=TransactionType.ROWS,
            direction=TransactionDirection.CHANGE,
            description='New line'
        )
        return HttpResponse(status=201)  # Created
    except json.JSONDecodeError:
        return HttpResponse(status=400)  # Bad Request
    except ValueError:
        return HttpResponse(status=404)  # Not Found
    except RuntimeError:
        return HttpResponse(status=500)  # Internal Server Error

@require_POST
def new_source(request, dataset_slug):
    """
    :param request:
    new_value - json with new line example {"source_file_slug": "slug", "position": "TAIL/HEAD"}
    :return:
    """
    required_params = [ 'source_file_pk']
    if not all(param in request.POST for param in required_params):
        return HttpResponse(status=400)  # Bad Request

    try:
        process_transaction(
            dataset_slug=dataset_slug,
            location_value="generic", #request.POST['position'],
            data_field={"new_data": request.POST['source_file_pk']},
            transaction_type=TransactionType.SOURCE,
            direction=TransactionDirection.CHANGE,
            description='New source'
        )
        return HttpResponse(status=201)  # Created
    except ValueError:
        return HttpResponse(status=404)  # Not Found
    except RuntimeError:
        return HttpResponse(status=500)  # Internal Server Error



@require_POST
def delete_source(request, dataset_slug):
    """
    :param request:
    new_value - json with new line example {"source_file_pk": pk}
    :return:
    """
    if 'source_file_pk' not in request.POST:
        return HttpResponse(status=400)  # Bad Request

    try:
        process_transaction(
            dataset_slug=dataset_slug,
            location_value=None,
            data_field={"delete_source": request.POST['source_file_pk']},
            transaction_type=TransactionType.SOURCE,
            direction=TransactionDirection.REMOVE,
            description='Delete source'
        )
        return HttpResponse(status=204)  # No Content
    except ValueError:
        return HttpResponse(status=404)  # Not Found
    except RuntimeError:
        return HttpResponse(status=500)  # Internal Server Error


