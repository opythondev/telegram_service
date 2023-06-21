import datetime
from typing import Any

from redis import Redis
from .local_task_storage import LocalTaskStorage
from .task import _Task


class TaskManager:

    def __init__(self, broker: Redis | None):
        self.storage = LocalTaskStorage({})
        self.broker = broker

    async def create_task(self, foo: Any, trigger: str, run_time: datetime, seconds: int = 0, kwarg: dict = None):

        match trigger:
            case "date":
                return _Task(foo=foo, trigger="date",
                         run_time=datetime.datetime.now() + datetime.timedelta(seconds=), kwargs={"uid": 233652006})
    async def add_task(self, task: _Task):
        self.storage.__dict__["storage"][str(task.task_id)] = task
        return task

    async def removed(self, task_id: str):
        self.storage.__dict__['storage'].pop(task_id)

    async def run_task(self, tasks: list[_Task]):
        for task in tasks:
            scheduler.add_job(task.foo, kwargs=task.kwargs)
            await self.removed(task_id=str(task.task_id))

    async def get_total_task(self):
        return len(self.storage.__dict__['storage'])

    async def run(self):
        date = datetime.datetime.now()
        executed_task = []

        for task_id, task in self.storage.storage.items():
            run_date = date - task.run_time

            if not "day" in str(run_date):
                executed_task.append(task)

        if executed_task:
            await self.run_task(tasks=executed_task)