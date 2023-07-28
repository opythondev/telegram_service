from celery import Celery

default_queue = Celery("default", broker='redis://localhost:6379/1')
db_queue = Celery("db_queue", broker='redis://localhost:6379/1')





