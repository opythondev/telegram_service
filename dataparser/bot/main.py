import logging

from telethon import TelegramClient

from bot.configs.env import API_ID, API_HASH
from bot.msg_broker.broker_listener import init_task_listener


async def __on_start_up():
    # INIT SUBSCRIBE WITH JOB BROKER
    await init_task_listener()


def start_bot():
    logging.basicConfig(level=logging.INFO)
    client = TelegramClient('anon', API_ID, API_HASH)
    client.loop.create_task(__on_start_up())
    logging.info("START BOT -> dataparser")
    client.loop.run_forever()


if __name__ == "__main__":
    start_bot()
