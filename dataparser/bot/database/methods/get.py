from sqlalchemy import and_, or_
from sqlalchemy.future import select
from bot.database.main import async_session_maker
from bot.database.models.channel import Channel
from bot.database.models.task import Task


async def get_task_by_uid(uid: int, status: str = "create"):
    async with async_session_maker() as s:
        q = select(Task).filter(and_(Task.user_id == uid, Task.status == status))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_task_by_id(id: int):
    async with async_session_maker() as s:
        q = select(Task).filter(Task.id == id)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_task_item_by_id(uid: int, task_item_id: int):

    ...


async def get_channel_by_id(cid: int):
    async with async_session_maker() as s:
        q = select(Channel).filter(Channel.id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


