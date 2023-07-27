from celery import Celery

from database.models.task import TaskData
from service.s_task import STask

default_queue = Celery("default", broker='redis://localhost:6379/1')


@default_queue.task
async def add_task_to_queue(task_data: TaskData):
    task = STask(task_data=task_data)
    return await task.send_task_to_bot()
