from bot.database.models.task import TaskData
from bot.database.methods.post import add_item, add_item_autoincrement
from bot.database.methods.get import get_task_by_uid
from bot.database.methods.put import update_task_by_id
from bot.database.models.task_item import TaskItemData
from bot.tasks import db_queue


class Database:

    def __init__(self, uid: int):
        self.uid = uid

    @staticmethod
    @db_queue.task
    async def add_task_item(task_item: TaskItemData):
        return await add_item_autoincrement(task_item)

    @staticmethod
    @db_queue.task
    async def update_task(task_id: int, update_data: dict):
        await update_task_by_id(task_id=task_id, data=update_data)

    async def get_task_by_id(self, task_id: int):
        # return get_task_by_uid()
        ...
