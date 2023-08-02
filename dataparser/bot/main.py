import asyncio
import logging
from bot.msg_broker.broker_listener import init_task_listener


def start_bot():
    logging.basicConfig(level=logging.INFO)
    logging.info("START PARSER_DATA")
    loop = asyncio.get_event_loop()
    loop.create_task(init_task_listener())
    loop.run_forever()


if __name__ == "__main__":
    start_bot()
