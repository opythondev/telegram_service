from database.models.task import TaskData
from database.methods.post import add_item_autoincrement


class Database:

    def __init__(self, uid: int):
        self.uid = uid

    async def add_task(self, task: TaskData):
        return await add_item_autoincrement(task)
