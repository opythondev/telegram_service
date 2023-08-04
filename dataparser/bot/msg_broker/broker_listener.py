import json
from bot.database.Redis import RedisClient
from ..parser_data.ParserData import ParserData


async def init_task_listener():
    redis = RedisClient()

    listener = await redis.create_listener_api_task()

    for task in listener.listen():
        if task['type'] == "message":
            data = json.loads(task["data"])
            parser = ParserData(uid=int(data['user_id']))
            await parser.start_parse_event(data=data)
