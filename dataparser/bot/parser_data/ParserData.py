from bot.database.models.task_item import TaskItemData
from bot.parser_data.utils import convert_dict_to_task
from .utils import convert_task_item_to_dict, convert_dict_to_task_item
from bot.tasks import add_task_item_in_db, add_parse_task
from bot.database.methods.main import Database


class ParserData:

    def __init__(self, uid: int):
        self.uid = uid
        self.db = Database(uid=uid)

    async def start_parse_event(self, data: dict):
        task = await convert_dict_to_task(data)

        for target_url in task.urls.split("::"):

            task_item = TaskItemData(task_id=task.id,
                                     target_url=target_url,
                                     channel_id=0,
                                     id=0,
                                     status="created")

            task_item = await convert_task_item_to_dict(task_item)
            task_item_data_with_id = add_task_item_in_db.delay(task_item)

    async def start_parsing(self, task_item: dict):
        task = await convert_dict_to_task_item(task_item=task_item)


class GroupParser:

    def __init__(self, uid: int, task_data: TaskItemData):
        self.task_data = task_data
        self.db = Database(uid=uid)

    async def _join(self):
        ...

    async def get_all_user(self):
        ...

    async def get_all_messages(self):
        ...





