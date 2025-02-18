import os
from celery import Celery
from dotenv import load_dotenv
from .tasks import infer


# Running as standalone module configures locally
if __name__ == "main":
    load_dotenv("../.env")

app = Celery('inference', broker=os.getenv("broker_url"))


@app.task
def infer_wrapper(processing_request_id: int):
    infer(processing_request_id)
