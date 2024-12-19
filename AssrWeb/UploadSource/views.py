from json import loads
from django.core.paginator import Paginator
from django.db.models import Q, QuerySet
from django.http.response import HttpResponse, JsonResponse
from django.http import StreamingHttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.views import View
from django.http import JsonResponse
from DjangoAssr.settings import PER_PAGE

from UploadSource.forms.SourceMetadataForm import SourceMetadataForm
from UploadSource.models import SourceTags, SourceMetadata, SourceFile
from UploadSource.file_checker import FileChecker
from .source_content_creator import ContentCreator
from UploadSource.forms import SourceSearchForm
from .CSVTableAsHTML import CSVTableAsHTML


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


def _get_paginated_source_files(filter_contains="",
                                page_number=0) -> QuerySet:

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


def list_page_view(request):
    search_form = SourceSearchForm()
    search_query = request.GET.get('search_query', None)

    context = {
        'form': search_form,
        'page': 'Исходники',
        'create_name': "Исходник",
        'link': "source:details",
        'addition_link': 'source:new-source',
    }

    selected_tags = request.GET.getlist('tags')

    if search_query is None and len(selected_tags) == 0:
        all_datasets = SourceMetadata.objects.order_by('name')
        paginator = Paginator(all_datasets, 8)
    else:
        search_result = SourceMetadata.objects.filter(
            Q(name__contains=search_query)
        )
        if search_query is not None and len(selected_tags) != 0:
            selected_tags = [
                i for i in SourceTags.objects.filter(Q(name__in=selected_tags))
            ]
            search_result = SourceMetadata.objects.filter(
                Q(name__contains=search_query) & Q(tag__in=selected_tags)
            )
        paginator = Paginator(search_result, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj

    return render(request, "SourceFiles/source-list.html", context)


def details_page_view(request, metadata_id):
    metadata = get_object_or_404(SourceMetadata, pk=metadata_id)
    sourceFile = get_object_or_404(SourceFile, metadata=metadata)

    key_values = []
    for i in sourceFile.metadata.keyValue.keys():
        key_values.append({"key": i, "value": sourceFile.metadata.keyValue[i]})
    creator = ContentCreator([sourceFile.ancestorFile])
    output = creator.to_html_embed()

    context = {
        "form": SourceMetadataForm(),
        "object": sourceFile,
        'key_value': key_values,
        "output": output,
        "meta": metadata_id,
    }
    return render(request, "SourceFiles/details.html", context)


def delete_view(request, metadata_id):
    metadata = get_object_or_404(SourceMetadata, pk=metadata_id)
    metadata.delete()
    return redirect('source:source-list')


class Details_page(View):
    """CBV for source-file page """
    render_step = 100  # hardcoded value of number of rows to be send

    def post(self, request, *args, **kwargs):
        data = loads(request.body)
        rows = int(data['last-row'])

        metadata = get_object_or_404(
            SourceMetadata,
            pk=kwargs['metadata_id']
        )
        sourceFile = get_object_or_404(SourceFile, metadata=metadata)
        html_info = CSVTableAsHTML(sourceFile.ancestorFile)

        # return JsonResponse({
        #     "rows-html": html_info.getNRows(rows, self.render_step),
        # })
        return StreamingHttpResponse(
            html_info.getNRows(rows, self.render_step),
            content_type='text/event-stream'
        )

    def get(self, request, *args, **kwargs):
        metadata = get_object_or_404(
            SourceMetadata,
            pk=kwargs['metadata_id']
        )
        sourceFile = get_object_or_404(SourceFile, metadata=metadata)
        html_info = CSVTableAsHTML(sourceFile.ancestorFile)

        context = {
            "tableHeader": html_info.getHeader()
        }

        return render(request, 'SourceFiles/testajax.html', context)
