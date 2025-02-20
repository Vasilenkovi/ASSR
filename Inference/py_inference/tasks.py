import logging
import time
from typing import Optional
from transformers import Pipeline, pipeline
from models import Processing_Manager, Dataset_Manager, File_reader
from mongo_connection import save_dict


def infer(processing_request_id: int):

    logging.info(f"accepted task: {processing_request_id}")
    starting_time = time.monotonic()
    
    # Read all inputs
    processing_task = Processing_Manager(processing_request_id)
    processing_record = processing_task.get_processing_record()

    model = processing_record.model_name
    parameters: dict = processing_record.extra_parameters
    tokenizer: Optional[str] = parameters.get("tokenizer")
    task: Optional[str] = parameters.get("task")
    column_ids: Optional[list[int]] = parameters.get("column_ids")

    # Leave only specifc model parameters
    TO_DROP = {"tokenizer", "task", "column_ids"}
    model_kw = {k: parameters[k] for k in parameters.keys() - TO_DROP}

    task.update_status(
        Processing_Manager.Status.Running
    )
    
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
            tokenizer=tokenizer,
            **model_kw
        )
    except RuntimeError as e:
        send_fail_message(
            processing_task,
            "Check tokenizer and/or task for given model",
            out_dict,
            f"pipeline init fail for task: {processing_request_id}"
        )

        return

    # Prepare and process files
    dataset = Dataset_Manager(processing_record.dataset_id)
    
    for file in dataset.get_file():
        file_iterator = File_reader(file.binary_file, column_ids)

        file_dict = {
            "file_id": file.id,
            "type": file_iterator.file_type.name,
            "samples": []
        }

        for sample_converter in file_iterator.get_sample():
            model_input = sample_converter.input_str

            model_output: object
            try:
                model_output = pipe(model_input)
            except TypeError as e:
                send_fail_message(
                    processing_task,
                    f"Unrecognized additional parameters for model",
                    out_dict,
                    f"pipeline call fail for task: {processing_request_id}"
                )

                return

            sample_dict = sample_converter.save(model_output)
            file_dict["samples"].append(sample_dict)

        out_dict["files"].append(file_dict)
    
    save_dict("processing", out_dict)
    task.update_status(
        Processing_Manager.Status.Successful
    )
    time_elapsed = time.monotonic() - starting_time
    logging.info(f"completed task: {processing_request_id} in {time_elapsed}s")


def send_fail_message(
        task: Processing_Manager, str_message: str,
        dict_to_save: dict, logger_message: str
    ):

    task.update_status(
        Processing_Manager.Status.Failed
    )
    dict_to_save["error_message"] = str_message
    save_dict("processing", dict_to_save)
    logging.error(logger_message)
