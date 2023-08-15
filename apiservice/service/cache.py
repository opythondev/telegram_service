import json

from database.methods.main import Database
from database.redis import RedisClient


class Cache:

    def __init__(self):
        self._redis = RedisClient()
        self._db = Database()

    async def _set_users_by_channel_id(self, channel_id: int, data: str):
        await self._redis.set_cache_all_user_by_channel_id(channel_id=channel_id, data=data)
        return await self.get_users_by_channel_id(channel_id=channel_id)

    async def get_users_by_channel_id(self, channel_id: int):
        data = await self._redis.get_cache_all_user_by_channel_id(channel_id=channel_id)
        if data is None:
            id_users = await self._db.get_all_users_by_cin(cid=channel_id)
            if id_users:
                all_users = await self._db.get_users_by_list_id(ids=id_users)

                return await self._set_users_by_channel_id(channel_id=channel_id, data=str(json.dumps(all_users,
                                                                                                      indent=4)))
            else:
                return {}
        else:
            return json.loads(data)

    async def _set_last_msg(self, channel_id: int, data: str):
        await self._redis.set_last_messages(channel_id=channel_id, data=data)
        return await self.get_last_msg(channel_id=channel_id)

    async def get_last_msg(self, channel_id: int):
        messages = await self._redis.get_last_messages(channel_id=channel_id)
        if not messages and messages is not None:
            messages_in_db = await self._db.get_new_messages_by_channel_id(channel_id=channel_id)
            print("messages_in_db", messages_in_db)
            return await self._set_last_msg(channel_id=channel_id, data=str(json.dumps(messages_in_db, indent=4)))
        else:
            print("messages", messages)
            return messages
