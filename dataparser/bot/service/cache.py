import json

from bot.database.Redis import RedisClient
from bot.database.methods.main import Database


class Cache:

    def __init__(self):
        self._redis = RedisClient()
        self._db = Database()

    async def update_last_msg(self, channel_id: int):
        last_msg = await self._db.get_new_messages_by_channel_id(channel_id=channel_id)
        await self._redis.clean_obj(key=f"message:{channel_id}", data=str(json.dumps(last_msg)))
