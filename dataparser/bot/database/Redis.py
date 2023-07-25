import redis

from bot.configs.env import REDIS_HOST, REDIS_PORT, REDIS_PASS


class RedisClient:

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, db=0, password=REDIS_PASS, socket_timeout=None):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.socket_timeout = socket_timeout

    def _connect_redis(self):
        if self.password:
            return redis.Redis(host=self.host, port=self.port, db=self.db, password=self.password, decode_responses=True)
        else:
            return redis.Redis(host=self.host, port=self.port, db=self.db,
                               decode_responses=True)

    async def create_listener_api_task(self):
        with self._connect_redis() as redis_cli:
            listener = redis_cli.pubsub()
            listener.subscribe("tasks-api-to-dataparser")

            return listener

