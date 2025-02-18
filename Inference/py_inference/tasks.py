from json import loads
from transformers import Pipeline, pipeline
from models import Processing_Manager, Dataset_Manager, File_reader
from mongo_connection import save_dict


def infer(processing_request_id: int):
    
    # Read all inputs
    processing_task = Processing_Manager(processing_request_id)
    processing_record = processing_task.get_processing_record()

    model = processing_record.model_name
    parameters: dict = loads(processing_record.parameters)
    tokenizer: str | None = parameters.get("tokenizer")
    task: str | None = parameters.get("tokenizer")
    column_ids: list[int] | None = parameters.get("column_ids")
    
    # Declare output document
    out_dict = {
        "processing_id": processing_record.id,
        "error_message": None,
        "files": []
    }

    # Prepare model
    pipe: Pipeline

    try:
        pipe = pipeline(
            task=task,
            model=model,
            tokenizer=tokenizer
        )
    except RuntimeError as e:
        processing_task.update_status(
            Processing_Manager.Status.Failed
        )
        out_dict["error_message"] = "Check tokenizer and/or task for given model"
        save_dict("processing", out_dict)

        return

    # Prepare and process files
    dataset = Dataset_Manager(processing_record.dataset.id)
    
    for file in dataset.get_file():
        file_iterator = File_reader(file.binary_file, column_ids)

        file_dict = {
            "file_id": file.id,
            "type": file_iterator.file_type,
            "samples": []
        }

        for sample_converter in file_iterator.get_sample():
            model_input = sample_converter.input_str
            model_output = pipe(model_input)
            sample_dict = sample_converter.save(model_output)
            file_dict["samples"].append(sample_dict)

        out_dict["files"].append(file_dict)
