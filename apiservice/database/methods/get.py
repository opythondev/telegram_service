from sqlalchemy import and_
from sqlalchemy.future import select
from database.main import async_session_maker
from database.models.channel import Channel
from database.models.posts import Post
from database.models.task import Task
from database.models.user import User
from database.models.user_channel import UserChannel


async def get_new_task_by_uid(uid: int):
    async with async_session_maker() as s:
        q = select(Task).filter(and_(Task.user_id == uid, Task.status == "new"))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_userchannel_by_cid(cid: int):
    async with async_session_maker() as s:
        q = select(UserChannel).filter(UserChannel.channel_id == cid)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_channels():
    async with async_session_maker() as s:
        q = select(Channel)
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_all_users_by_list_id_(ids: list[int]):
    async with async_session_maker() as s:
        q = select(User).where(User.id.in_(ids))
        data = await s.execute(q)
        curr = data.scalars()
    return curr


async def get_new_msg_by_cin(cin: int):
    async with async_session_maker() as s:
        q = select(Post).filter(and_(Post.channel_id == cin, Post.state == "new", Post.type == "Text"))
        data = await s.execute(q)
        curr = data.scalars()
    return curr
