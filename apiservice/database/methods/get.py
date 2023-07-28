from sqlalchemy import and_, or_
from sqlalchemy.future import select
from database.main import async_session_maker
from database.models.task import Task


async def get_new_task_by_uid(uid: int):
    async with async_session_maker() as s:
        q = select(Task).filter(and_(Task.user_id == uid, Task.status == "new"))
        data = await s.execute(q)
        curr = data.scalars()
    return curr
