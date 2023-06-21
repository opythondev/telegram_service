from telethon import TelegramClient

from .configs.env import API_ID, API_HASH


async def __on_start_up():
    print("start get tasks que")


def start_bot():
    # TODO организовать проверку файла с сессией, если нет то сделать подключение и ответить на смс

    client = TelegramClient('anon', API_ID, API_HASH)
    client.loop.create_task(__on_start_up())
    client.loop.run_forever()