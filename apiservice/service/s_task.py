from database.models.task import TaskData, Task
from database.methods.main import Database
from database.redis import RedisClient


class STask:

    def __init__(self, task_data: TaskData):
        self.task_data = task_data
        self.db = Database(task_data.user_id)
        self.redis_cli = RedisClient()

    async def send_task_to_bot(self):
        db_entity = Task(self.task_data)
        task_id = await self.db.add_task(db_entity)
        self.task_data.id = task_id

        await self.redis_cli.pub_task(f"new_job_for::bot", await self._convert_task_to_dict(self.task_data))

        return self.task_data

    async def _convert_task_to_dict(self, task: TaskData):

        return {"type": task.type,
                "user_id": task.user_id,
                "urls": task.urls,
                "id": task.id,
                "status": task.status,
                "create_at": str(task.create_at)}
