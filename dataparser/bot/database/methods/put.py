
import logging
from datetime import datetime

from sqlalchemy import update

from bot.database.main import async_session_maker
from bot.database.models.task import Task
from bot.database.models.task_item import TaskItem


async def update_task_by_id(task_id: int, data: dict):
    async with async_session_maker() as s:
        async with s.begin():

            stmt = update(Task).\
                where(Task.id == task_id).\
                values(data).\
                execution_options(synchronize_session="fetch")

            await s.execute(stmt)
            await s.commit()
            logging.info(f"item update task ID: {task_id}in data base {datetime.now()}")


async def update_task_item_by_id(task_item_id: int, data: dict):
    async with async_session_maker() as s:
        async with s.begin():
            q = update(
                TaskItem)\
                .filter(TaskItem.id == task_item_id)\
                .values(data)\
                .execution_options(synchronize_session="fetch")
            await s.execute(q)
            await s.commit()
            logging.info(f"item update task ID: {task_item_id}in data base {datetime.now()}")