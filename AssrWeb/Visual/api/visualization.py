from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ProcessingApp.models import Processing_model
from ..Plotting.PlotGenerator import PlotGenerator
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import base64


@require_GET
def get_all_figures(request, task_pk):
    process = get_object_or_404(Processing_model, pk=task_pk)

    if process.status != Processing_model.Status.Suc:
        return JsonResponse({"error": "Results not ready"}, status=404)

    try:
        plot_generator = PlotGenerator(process)
        figures = plot_generator.get_all_available_figures()
        interactive = request.GET.get('interactive', 'false').lower() == 'true'
        response_data = {"visualizations": [], "labels": []}
        label_set = set()

        for fig in figures:

            if interactive:
                content = fig.get_interactive()
                vis_type = "interactive"
            else:
                content = base64.b64encode(fig.get_image()).decode('utf-8')
                vis_type = "image"

            label = getattr(fig, 'label', None)
            group_type = "distribution" if label else None
            if label:
                label_set.add(label)

            metadata = {
                "name": fig.name,
                "type": vis_type,
                "label": label,
                "group_type": group_type
            }

            response_data["visualizations"].append({
                "content": content,
                "meta": metadata
            })

        response_data["labels"] = list(label_set)

        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_GET
def download_visualization(request, task_pk):
    process = get_object_or_404(Processing_model, pk=task_pk)
    vis_name = request.GET.get('vis_name')
    file_format = request.GET.get('format', 'png')

    plot_generator = PlotGenerator(process)
    figures = plot_generator.get_all_available_figures()

    for vis in figures:
        if vis.name == vis_name:
            file_data = vis.get_file_in_format(file_format)
            response = HttpResponse(
                file_data,
                content_type=f'image/{file_format}'
            )
            response['Content-Disposition'] = 'attachment;' + f'filename="{vis_name}.{file_format}"'
            return response

    return JsonResponse({"error": "Visualization not found"}, status=404)
