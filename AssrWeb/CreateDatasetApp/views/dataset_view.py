from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Value
from django.http import HttpResponse
from django.db.models import Q
from json import loads
from django.http import StreamingHttpResponse
from django.views import View

from CreateDatasetApp.forms import DatasetMetadataForm, DatasetSearchForm
from CreateDatasetApp.models import DatasetFile, DatasetMetadata, DatasetTags
from MetaCommon.ContentCreator import ContentCreator


def show_list(request):
    search_form = DatasetSearchForm()
    search_query = request.GET.get('search_query', None)
    context = {
        'form': search_form,
        'page': 'Датасеты',
        'create_name': "Датасет",
        'link': 'dataset:view_dataset',
        'addition_link': "dataset:new-source",
    }
    selected_tags = request.GET.getlist('tag')
    if search_query is None and len(selected_tags) == 0:
        all_datasets = DatasetMetadata.objects.order_by('name')
        paginator = Paginator(all_datasets, 8)
    else:
        search_result = DatasetMetadata.objects.filter(Q(name__contains=search_query))
        if search_query is not None and len(selected_tags) != 0:
            selected_tags = [i for i in DatasetTags.objects.filter(Q(pk__in=selected_tags))]
            search_result = DatasetMetadata.objects.filter(Q(name__contains=search_query) & Q(tag__in=selected_tags))
        paginator = Paginator(search_result, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(request, "Datasets/dataset-list.html", context)


def dataset_download(request, dataset_slug):
    csv_file = get_object_or_404(DatasetFile, id=dataset_slug)
    response = HttpResponse(csv_file.currentFile, content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{csv_file.metadata.name}.csv"'
    return response


class Dataset_Details(View):
    """CBV for dataset page"""
    render_step = 100  # hardcoded value of number of rows to be send

    def post(self, request, *args, **kwargs):
        data = loads(request.body)
        rows = int(data['last-row'])

        dataset = DatasetFile.objects.filter(
            metadata__pk=kwargs['dataset_slug']
        ).get()
        file = dataset.currentFile
        cc = ContentCreator([file])

        return StreamingHttpResponse(
            cc.getNRows(rows, self.render_step),
            content_type='text/event-stream'
        )

    def get(self, request, *args, **kwargs):
        dataset = DatasetFile.objects.filter(
            metadata__pk=kwargs['dataset_slug']
        ).get()
        key_values = []
        for i in dataset.metadata.keyValue.keys():
            key_values.append(
                {"key": i, "value": dataset.metadata.keyValue[i]}
            )
        file = dataset.currentFile
        html_info = ContentCreator([file])
        context = {
            'form': DatasetMetadataForm(),
            'object': dataset,
            'key_value': key_values,
            'tableHeader': html_info.getHeader(),
            'source_files': dataset.source_list.all().annotate(
                checked=Value(True)
            ),
            "data_type": html_info.type
        }

        return render(request, "Datasets/dataset-view.html", context)
