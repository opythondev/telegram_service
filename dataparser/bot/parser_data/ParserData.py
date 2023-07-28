import datetime

from bot.database.models.task import TaskData
from bot.database.models.task_item import TaskItemData, TaskItem
from bot.tasks import default_queue
from bot.database.methods.main import Database


class ParserData:

    def __init__(self, uid: int):
        self.uid = uid
        self.db = Database(uid=uid)

    async def prepare_tasks_for_queue(self, data: dict):
        task = await self._convert_dict_to_task(data)

        await self.db.update_task(task_id=task.id, update_data={
            "status": "process"
        })

        for target_url in task.urls.split("::"):

            task_item = TaskItemData(task_id=task.id,
                                     target_url=target_url,
                                     channel_id=0,
                                     id=0,
                                     status="created",
                                     create_at=datetime.datetime.utcnow(),
                                     finished_at=datetime.datetime.utcnow())

            await self.db.add_task_item(TaskItem(task_item=task_item))

    async def _convert_dict_to_task(self, data: dict):
        return TaskData(type=data['type'],
                        user_id=data['user_id'],
                        urls=data['urls'],
                        id=data['id'],
                        status=data['status'],
                        create_at=data['create_at'])
