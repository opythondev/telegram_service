from bot.database.models.task_item import TaskItemData
from bot.parser_data.utils import convert_dict_to_task
from .utils import convert_task_item_to_dict
from bot.tasks import add_task_item_in_db, start_parsing_task
from bot.database.methods.main import Database


class ParserData:

    def __init__(self, uid: int):
        self.uid = uid
        self.db = Database(uid=uid)

    async def start_parse_event(self, data: dict):
        task = await convert_dict_to_task(data)

        # TODO fix update func
        # await self.db.update_task(task_id=task.id, update_data={"status": "process"})

        for target_url in task.urls.split("::"):

            task_item = TaskItemData(task_id=task.id,
                                     target_url=target_url,
                                     channel_id=0,
                                     id=0,
                                     status="created")

            task_item_data_with_id = add_task_item_in_db.delay(task_item.to_dict()).get()

            task_item_data_with_id['raw_data']['id'] = task_item_data_with_id['task_item_id']
            task_item_data_with_id['raw_data']['uid'] = task.user_id

            await self.add_task_to_parsing_queue(task_item=task_item_data_with_id)

    async def add_task_to_parsing_queue(self, task_item: dict):

        task_item_update = {
            "status": "process"
        }

        await self.db.update_task_item(task_item_id=task_item['raw_data']['id'], update_data=task_item_update)

        return start_parsing_task.delay(task_item=task_item['raw_data']).get()






