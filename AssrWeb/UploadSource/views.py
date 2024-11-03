from json import loads
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from UploadSource.forms.SourceMetadataForm import SourceMetadataForm
from UploadSource.models import SourceMetadata, SourceFile
from UploadSource.file_checker import FileChecker
import base64

# Create your views here.
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

    try:
        metadata_obj = SourceMetadata.objects.create(
            name = metadata["name"],
            author = metadata["author"],
            keyValue = metadata["key_value"]
        )
        metadata_obj.tag.set( metadata["tags"])
        metadata_obj.save()

        SourceFile.objects.create(
            ancestorFile = request.FILES["file"].file.read(), # Get actual binary
            metadata = metadata_obj
        )

        return HttpResponse(status=200)

    except TypeError:
        return HttpResponse(status=500)

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
