from bot.database.methods.post import add_item, add_item_autoincrement
from bot.database.methods.get import get_task_by_uid
from bot.database.methods.put import update_task_by_id
from bot.database.models.task_item import TaskItemData, TaskItem
from bot.parser_data.utils import convert_dict_to_task_item, convert_task_item_to_dict


class Database:

    def __init__(self, uid: int = None):
        self.uid = uid

    async def add_task_item(self, task_item: dict):

        return {"status": 200,
                "task_item_id": int(await add_item_autoincrement(TaskItem(await convert_dict_to_task_item(task_item)))),
                "raw_data": task_item
                }

    async def update_task(self, task_id: int, update_data: dict):

        await update_task_by_id(task_id=task_id, data=update_data)

