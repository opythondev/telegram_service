from database.models.task import Task
from database.methods.main import Database
from database.redis import RedisClient
from router.utils import convert_dict_to_task


class STask:

    def __init__(self, task_data: dict):
        self.task_data = task_data
        self.db = Database()
        self.redis_cli = RedisClient()

    async def send_task_to_bot(self):

        db_entity = Task(await convert_dict_to_task(self.task_data))
        task_id = await self.db.add_task(db_entity)
        self.task_data["id"] = task_id

        await self.redis_cli.pub_task("new_job_for::bot", self.task_data)

        return self.task_data
