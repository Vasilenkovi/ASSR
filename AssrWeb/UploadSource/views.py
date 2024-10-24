from json import loads
from django.http.response import HttpResponse
from django.shortcuts import render
from django.db import IntegrityError
from UploadSource.forms.SourceMetadataForm import SourceMetadataForm
from UploadSource.models import SourceMetadata, SourceFile

# Create your views here.
def upload_page_view(request):
    context = {
        "metadataForm": SourceMetadataForm()
    }

    return render(request, "SourceFiles/create.html", context)

def upload_endpoint_view(request):
    metadata = loads(request.POST["metadata"])

    try:
        metadata_obj = SourceMetadata.objects.create(
            name = metadata["name"],
            author = metadata["author"],
            keyValue = metadata["key_value"]
        )
        metadata_obj.tag.set( metadata["tags"])
        metadata_obj.save()

        source_file_obj = SourceFile.objects.create(
            ancestorFile = request.FILES["file"].file.read(), # Get actual binary
            metadata = metadata_obj
        )

        return HttpResponse(status=200)

    except (TypeError) as e:
        return HttpResponse(status=500)
