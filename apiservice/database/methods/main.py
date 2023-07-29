from database.models.task import TaskData
from database.methods.post import add_item, add_item_autoincrement
from database.methods.get import get_new_task_by_uid
from tasks import default_queue
from router.utils import convert_dict_to_task


class Database:

    def __init__(self, uid: int):
        self.uid = uid

    async def add_task(self, task: TaskData):
        return await add_item_autoincrement(task)
