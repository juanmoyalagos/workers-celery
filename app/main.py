import os
from dotenv import load_dotenv

# FastAPI
from fastapi import FastAPI

# celery
from celery import Celery
from celery_config.tasks import wait_and_return, sum_to_n_job
from models import Number

load_dotenv('.env')

app = FastAPI()

celery_app = Celery(
    __name__,
    # https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/index.html
    broker=os.environ.get('CELERY_BROKER_URL', ''),
    backend=os.environ.get('CELERY_RESULT_BACKEND', '')
)

# Setup to use all the variables in settings
# that begins with 'CELERY_'
celery_app.config_from_object('celery_config.config', namespace='CELERY')

@app.get("/")
def read_root():
    return {"Hello": "World"}

# https://docs.celeryq.dev/en/stable/getting-started/first-steps-with-celery.html
@app.get("/wait_and_return")
def get_publish_job():
    job = wait_and_return.delay()
    return {
        "message": "job published",
        "job_id": job.id,
    }

@app.get("/wait_and_return/{job_id}")
def get_job(job_id: str):
    job = wait_and_return.AsyncResult(job_id)
    print(job)
    return {
        "ready": job.ready(),
        "result": job.result,
    }

@app.post("/job")
def post_publish_job(number: Number):
    job = sum_to_n_job.delay(number.number)
    return {
        "message": "job published",
        "job_id": job.id,
    }

@app.get("/job/{job_id}")
def get_job(job_id: str):
    job = sum_to_n_job.AsyncResult(job_id)
    print(job)
    return {
        "ready": job.ready(),
        "result": job.result,
    }
