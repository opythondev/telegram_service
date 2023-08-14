import json
from typing import Any

from database.methods.main import Database
from database.models.channel import ChannelData
from database.models.user_channel import UserChannel
from service.cache import Cache


class ChannelFabric:

    async def create_user_channel(self, user_channel_data: Any) -> list[UserChannel]:
        ...

    async def create_channels(self, channels: Any) -> list[ChannelData]:

        ...


class ChannelService:

    def __init__(self, channel_id: int | None = None):
        self.channel_id = channel_id
        self._db = Database()
        self._cache = Cache()

    async def get_all_channels(self) -> dict:
        return await self._db.get_all_channels()

    async def get_all_users(self) -> dict:
        return await self._cache.get_users_by_channel_id(channel_id=self.channel_id)

    async def get_last_msg(self) -> dict:
        return json.loads(await self._cache.get_last_msg(channel_id=self.channel_id))
