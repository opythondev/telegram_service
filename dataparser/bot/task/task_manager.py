import datetime
import uuid
import pickle
from typing import Any, Union
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from celery.app import Celery
from bot.database.Redis import RedisClient

from redis import Redis
from .local_task_storage import LocalTaskStorage
from .task import _Task

scheduler = AsyncIOScheduler()


class TaskManager:

    def __init__(self, broker: Redis | None = None):
        self.storage = LocalTaskStorage({})
        self.broker = broker

    async def create_task_(self, foo: Any, trigger: str | None = None,
                           run_time: Union[datetime.datetime, None] = None,
                           kwarg: dict = None) -> _Task:

        match trigger:

            case "date":
                task_id = uuid.uuid4()
                return _Task(foo=foo, trigger="date", task_id=task_id,
                             run_time=run_time, kwargs=kwarg)
            case "now":
                task_id = uuid.uuid4()
                return _Task(foo=foo, trigger="date", run_time=datetime.datetime.now() + datetime.timedelta(seconds=1),
                             task_id=task_id, kwargs=kwarg)

    async def add_local_task(self, task: _Task):
        self.storage.__dict__["storage"][str(task.task_id)] = task
        return task

    async def remove_local_task(self, task_id: str):
        self.storage.__dict__['storage'].pop(task_id)

    async def run_task(self, tasks: list[_Task]):

        for task in tasks:
            scheduler.add_job(task.foo, kwargs=task.kwargs)
            await self.remove_local_task(task_id=str(task.task_id))

    async def get_total_task(self):
        return len(self.storage.__dict__['storage'])

    async def save_storage_in_broker(self, stor: LocalTaskStorage):
        serialise = pickle.dumps(stor)
        self.broker.hset("storage", key="storage", value=serialise)

    async def load_storage_from_broker(self):
        stor = self.broker.hget("storage", key="storage")
        return pickle.loads(stor)

    async def run(self):
        date = datetime.datetime.now()
        executed_task = []

        for task_id, task in self.storage.storage.items():
            run_date = date - task.run_time

            if not "-1" in str(run_date):
                executed_task.append(task)

        if executed_task:
            await self.run_task(tasks=executed_task)


manager = TaskManager()


async def check_tasks(manager: TaskManager):
    await manager.run()


async def add_task_to_local_queue():
    redis = RedisClient()

    listener = await redis.create_listener_api_task()

    for msg in listener.listen():
        # await manager.create_task_(foo=, trigger="now")
        print(msg)

