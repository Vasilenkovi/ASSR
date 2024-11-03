from json import loads
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http.response import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from DjangoAssr.settings import PER_PAGE
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from UploadSource.forms.SourceMetadataForm import SourceMetadataForm
from UploadSource.models import SourceTags, SourceMetadata, SourceFile
from UploadSource.file_checker import FileChecker
import base64


def upload_page_view(request):
    context = {
        "metadataForm": SourceMetadataForm()
    }

    return render(request, "SourceFiles/create.html", context)


def upload_endpoint_view(request):

    checker = FileChecker(request.FILES["file"].file)
    if not checker.check():
        return HttpResponse(content="неверный формат файла", status=400)

    metadata = loads(request.POST["metadata"])

    if not metadata["name"]:
        return HttpResponseBadRequest("Name should not be blank")

    try:
        tags = SourceTags.objects.filter(
            name__in=metadata["tags"]
        )

        metadata_obj = SourceMetadata.objects.create(
            name=metadata["name"],
            author=metadata["author"],
            keyValue=metadata["key_value"]
        )
        metadata_obj.tag.set(tags)
        metadata_obj.save()

        request.FILES["file"].file.seek(0) # Reset file checker
        SourceFile.objects.create(
            ancestorFile=request.FILES["file"].file.read(), # Get actual binary
            metadata=metadata_obj
        )

        return HttpResponse(status=200)

    except TypeError:
        return HttpResponse(status=500)


@require_POST
def filter_source_view(request):

    context = {
        "source_files": _get_paginated_source_files(
            request.POST["contains"],
            int(request.GET.get("page"))
        )
    }

    html_safe = render_to_string("includes/sourceListTable.html", context)

    response = {
        "table_html": html_safe
    }

    return JsonResponse(response)


def _get_paginated_source_files(filter_contains = "",
                                page_number = 0) -> QuerySet:

    files = SourceFile.objects.prefetch_related("metadata")
    if filter_contains:
        tags = SourceTags.objects.filter(
            name__icontains=filter_contains
        )

        files = files.filter(
            Q(metadata__name__icontains=filter_contains) |
            Q(metadata__author__icontains=filter_contains) |
            Q(metadata__keyValue__icontains=filter_contains) |
            Q(metadata__tag__in=tags)
        )

    page_obj = Paginator(files, PER_PAGE)

    return page_obj.get_page(page_number)


def details_page_view(request, metadata_id):
    metadata = get_object_or_404(SourceMetadata, id=metadata_id)
    sourceFile = get_object_or_404(SourceFile, metadata=metadata)

    recived_data = sourceFile.ancestorFile
    file_data = base64.b64encode(sourceFile.ancestorFile).decode()

    context = {
        "metadata": metadata,
        "sourceFile": sourceFile,
        "file": file_data,
    }

    return render(request, "SourceFiles/details.html", context)
