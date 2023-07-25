import asyncio

from database.methods.main import Database
from database.models.task import TaskData, Task
from service.s_task import STask


test_data = {
    "type": "channel",
    "user_id": 233652006,
    "id": 0,
    "status": "new"
}
urls = "https://t.me/openvocallessons:https://t.me/fastapiru:https://t.me/ethernitycloud"


async def get_id():
    t_data = TaskData(type=test_data['type'], user_id=test_data['user_id'], status=test_data['status'])

    test_case = STask(task_data=t_data, urls=urls)
    task_id = await test_case.add_task_event()
    return task_id


def start():
    loop = asyncio.new_event_loop()
    loop.run_until_complete(get_id())


if __name__ == "__main__":
    start()
