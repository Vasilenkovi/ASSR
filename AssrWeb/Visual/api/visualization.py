from django.http import JsonResponse
from django.views.decorators.http import require_GET
from ProcessingApp.models import Processing_model
from ..Plotting.PlotGenerator import PlotGenerator
from django.shortcuts import get_object_or_404
import base64
@require_GET
def get_figures(request, task_pk):
    process = get_object_or_404(Processing_model, pk=task_pk)

    if process.status != Processing_model.Status.Suc:
        return JsonResponse({"error": "Results not ready"}, status=404)

    try:
        plot_generator = PlotGenerator(process)
        figures = plot_generator.get_all_available_figures()
        interactive = request.GET.get('interactive', 'false').lower() == 'true'
        print(figures)
        response_data = {"visualizations": []}
        for fig in figures:
            if interactive:
                content = fig.get_interactive()
                vis_type = "interactive"
            else:
                content = base64.b64encode(fig.get_image()).decode('utf-8')
                vis_type = "image"

            response_data["visualizations"].append({
                "name": fig.name,
                "type": vis_type,
                "content": content
            })
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)