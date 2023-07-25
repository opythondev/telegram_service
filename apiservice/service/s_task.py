from database.models.task import TaskData, Task
from database.methods.main import Database


class STask:

    def __init__(self, task_data: TaskData, urls: str):
        self.task_data = task_data
        self.urls = urls
        self.db = Database(task_data.user_id)

    async def add_task_event(self):
        type_, user_id, status = self.task_data.type,\
            self.task_data.user_id,\
            self.task_data.status
        task = await self._create_dataclass(type_=type_, user_id=user_id, status=status)
        return await self.send_task_to_bot(task=task, urls=self.urls)

    async def _create_dataclass(self, type_: str, user_id: int, status: str):
        task = TaskData(type=type_, user_id=user_id, status=status)
        return task

    async def transform_data_for_bot(self, data: TaskData, urls: str) -> dict:
        new_data = {"type": data.type,
                    "user_id": data.user_id,
                    "status": data.status,
                    "urls": urls}

        return new_data

    async def send_task_to_bot(self, task: TaskData, urls: str):
        entity_task = Task(task)
        task_id = await self.db.add_task(entity_task)

        data_for_bot = await self.transform_data_for_bot(task, urls)
        data_for_bot['id'] = task_id
        # send ...

        return data_for_bot
