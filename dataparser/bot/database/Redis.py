import redis

from bot.configs.env import REDIS_HOST, REDIS_PORT, REDIS_PASS


class RedisClient:

    def __init__(self,
                 host=REDIS_HOST,
                 port=REDIS_PORT,
                 db=0,
                 password=REDIS_PASS,
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

    async def create_listener_api_task(self):
        with self._connect_redis() as redis_cli:
            listener = redis_cli.pubsub()
            listener.subscribe("new_job_for::bot")

            return listener

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

    async def clean_obj(self, key: str, **kwargs):
        with self._connect_redis() as redis_cli:
            redis_cli.delete(key)

            if kwargs:
                redis_cli.set(key, kwargs['data'])
