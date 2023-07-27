import json

import redis
from config.env import R_PASS, R_HOST, R_PORT
from database.models.task import TaskData


class RedisClient:

    def __init__(self, host=R_HOST, port=R_PORT, db=0, password=R_PASS, socket_timeout=None):
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

    async def pub_task(self, chanel: str,  data: dict):
        with self._connect_redis() as redis_cli:
            redis_cli.publish(chanel, json.dumps(data, indent=4))

