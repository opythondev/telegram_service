import asyncio
from typing import Any
import functools
from bot.database.methods.main import Database

from celery import Celery


default_queue = Celery("default", broker='redis://localhost:6379/1',
                       backend='redis://localhost:6379/1',
                       include=['bot.tasks']
                       )


def run_async_task(func):
    @functools.wraps(func)
    def wrapper_run_async_task(*args, **kwargs):
        loop = asyncio.get_event_loop()

        return loop.run_until_complete(func(*args, **kwargs))

    return wrapper_run_async_task


@default_queue.task(serializer="json")
@run_async_task
def add_task_item_in_db(task_item: dict):
    db = Database()
    result = db.add_task_item(task_item=task_item)
    return result


@default_queue.task(serializer='json')
@run_async_task
def add_parse_task(task_data: dict):
    ...