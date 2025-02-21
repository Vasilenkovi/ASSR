import logging
import os
from celery import Celery
from dotenv import load_dotenv
from tasks import infer


# Running as standalone module configures locally
load_dotenv()

logging.basicConfig(
    format="[%(asctime)s] [%(levelname)s] [%(message)s]",
    level=logging.INFO
)

app = Celery('inference', broker=os.getenv("broker_url"))

@app.task(name="inference.celery.infer_wrapper")
def infer_wrapper(processing_request_id: int):
    infer(processing_request_id)
