import csv
import io
import json
import os

import pymongo
from bson import json_util
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from ProcessingApp.models import Processing_model


def _get_database():
    username  = os.getenv("mongo_username")
    password  = os.getenv("mongo_password")
    host_name = os.getenv("mongo_host_name")
    host_port = os.getenv("mongo_host_port")
    database  = os.getenv("mongo_database")
    
    url = f"mongodb://{username}:{password}@{host_name}:{host_port}"

    client = pymongo.MongoClient(url)
    return client[database]


def fetch_processing_result(task_pk):
    try:
        database = _get_database()
        result_data = database["processing"].find_one({"processing_id": int(task_pk)})
        if not result_data:
            return None, None
        json_response = json.dumps(
            result_data,
            default=json_util.default,
            indent=2,
            ensure_ascii=False
        )
        return result_data, json_response
    except pymongo.errors.PyMongoError as e:
        raise Exception(f"MongoDB error: {str(e)}")
    

def task_results(request, task_pk):
    process = get_object_or_404(Processing_model, pk=task_pk)
    context = {"status": process.status, 'process': process, 'task_pk': task_pk,}
    if process.status == Processing_model.Status.Suc:
        try:
            result_data, json_response = fetch_processing_result(task_pk)
            if result_data is None:
                return HttpResponse("404: Ooops, processing results not found \n ... \n Praise the Omnissiah", status=404)
            context["json_results"] = json_response
        except pymongo.errors.PyMongoError as e:
            return HttpResponse(f"MongoDB died from cringe with error: {str(e)} \n It's time to call technodebilus", status=500)
    return render(request, "Proccessing/results.html", context)


def download_processing_results(request, task_pk):
    file_format = request.GET.get('file_format')
    process = get_object_or_404(Processing_model, pk=task_pk)
    if process.status == Processing_model.Status.Suc:
        try:
            result_data, json_response = fetch_processing_result(task_pk)
            if result_data is None:
                return HttpResponse("Ooops, it seems that processing have ended with no results \n ... \n Damn these blood ravens, they stole your data", status=500)
        except pymongo.errors.PyMongoError as e:
            return HttpResponse(f"MongoDB died from cringe with error: {str(e)} \n It's time to call technodebilus", status=500)
    else:
        return HttpResponse("Ooops, processing results not found \n ... \n Praise the Omnissiah", status=404)
    match file_format:
            case 'CSV':
                try:
                    csv_buffer = json_to_csv(result_data)
                    response = HttpResponse(csv_buffer.getvalue(), content_type='text/csv')
                    response['Content-Disposition'] = f'attachment; filename="{process.pk}-results.csv"'
                except Exception as e:
                    return HttpResponse(f"Converter died from cringe with error: {str(e)} \n It's time to call technodebilus", status=500)
            case 'JSON':
                response = HttpResponse(
                    json_response, content_type='application/json'
                )
                response['Content-Disposition'] = (
                    f'attachment; filename="{process.pk}-results.json"'
                )
    return response


def json_to_csv(json_file):
    buffer = io.StringIO()
    writer = csv.writer(buffer, delimiter=';')
    writer.writerow(["file_id", "sample_number", "text"]) 
    
    for entry in json_file.get("files", []):  
        for i, sample in enumerate(entry.get("samples", [])):
            writer.writerow([
                entry.get("file_id", ""),
                f'sample {i}',
                json.dumps(sample, ensure_ascii=False)  
            ])
    
    return buffer
