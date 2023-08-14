from database.models.task import TaskData
from database.methods.post import add_item_autoincrement
from database.methods.get import get_channels, get_all_userchannel_by_cid, get_all_users_by_list_id_, get_new_msg_by_cin


class Database:

    async def add_task(self, task: TaskData):
        return await add_item_autoincrement(task)

    async def get_all_channels(self) -> dict:
        return {item.id: item for item in await get_channels()}

    async def get_all_users_by_cin(self, cid: int) -> list[int]:
        return [item.user_id for item in await get_all_userchannel_by_cid(cid=cid)]

    async def get_users_by_list_id(self, ids: list[int]) -> dict:
        return {item.id: {"id": item.id,
                          "full_name": item.full_name,
                          "user_name": item.user_name,
                          "phone": item.phone,
                          "email": item.email,
                          "create_at": str(item.create_at),
                          "is_subscribed": item.is_subscribed,
                          "role": item.role
                          } for item in await get_all_users_by_list_id_(ids=ids)}

    async def get_new_messages_by_channel_id(self, channel_id: int) -> dict:
        return {item.id: {
            "channel_id": item.channel_id,
            "id": item.id,
            "message_id": item.message_id,
            "text": item.text,
            "views_count": item.views_count,
            "reactions_count": item.reactions_count,
            "comments_channel_id": item.comments_channel_id,
            "type": item.type
        } for item in await get_new_msg_by_cin(cin=channel_id)
        }
