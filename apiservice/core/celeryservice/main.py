import os
from environs import Env
from datetime import datetime
from typing import List
from celery.app import Celery

# from ..core.utils.settings import settings

env = Env()
env.read_env()

redis_host = env.str("REDIS_HOST")
redis_password = env.str("REDIS_PASSWORD")

redis_url = f"redis://:{redis_password}@{redis_host}:6379"

celery_app = Celery("tasks", broker=redis_url, backend=redis_url)


@celery_app.task
def add_channel_list_to_worker(channels: List[str]):
    print("data: ", channels)


@celery_app.task
def dummy_task():
    folder = "/tmp/celery"
    os.makedirs(folder, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%s")
    with open(f"{folder}/task-{now}.txt", "w") as f:
        f.write("hello!")
