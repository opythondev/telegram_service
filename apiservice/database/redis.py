import json

import redis
from config.env import R_PASS, R_HOST, R_PORT


class RedisClient:

    def __init__(self,
                 host=R_HOST,
                 port=R_PORT,
                 db=0,
                 password=R_PASS,
                 socket_timeout=None):

        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.socket_timeout = socket_timeout

    def _connect_redis(self):
        if self.password:
            return redis.Redis(host=self.host,
                               port=self.port,
                               db=self.db,
                               password=self.password,
                               decode_responses=True)
        else:
            return redis.Redis(host=self.host,
                               port=self.port,
                               db=self.db,
                               decode_responses=True)

    async def pub_task(self, chanel: str, data: dict):
        with self._connect_redis() as redis_cli:
            redis_cli.publish(chanel, json.dumps(data, indent=4))

    async def set_cache_all_user_by_channel_id(self, channel_id: int, data: str):
        with self._connect_redis() as redis_cli:
            redis_cli.set(f"userchannel:{channel_id}", data)

        return await self.get_cache_all_user_by_channel_id(channel_id=channel_id)

    async def get_cache_all_user_by_channel_id(self, channel_id: int):
        with self._connect_redis() as redis_cli:
            data = redis_cli.get(f"userchannel:{channel_id}")
            return data

    async def set_last_messages(self, channel_id: int, data: str):
        with self._connect_redis() as redis_cli:
            redis_cli.set(f"messages:{channel_id}", data)

    async def get_last_messages(self, channel_id: int):
        with self._connect_redis() as redis_cli:
            data = redis_cli.get(f"messages:{channel_id}")
            return data
