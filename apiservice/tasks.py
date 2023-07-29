from celery import Celery

default_queue = Celery("default", broker='redis://localhost:6379/1')

