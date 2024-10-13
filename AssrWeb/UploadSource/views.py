from django.shortcuts import render
from UploadSource.forms.SourceMetadataForm import SourceMetadataForm

# Create your views here.
def upload_page_view(request):
    context = {
        "metadataForm": SourceMetadataForm()
    }

    return render(request, "SourceFiles/create.html", context)