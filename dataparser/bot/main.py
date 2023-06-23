import logging

from telethon import TelegramClient

from .configs.env import API_ID, API_HASH
from .task.task_manager import scheduler, manager, check_tasks
from .task.test_tasks import create_fake_task


async def __on_start_up():

    logging.info("INIT on_start_up")

    scheduler.add_job(func=create_fake_task, trigger="cron", minute="*/1")
    scheduler.add_job(func=check_tasks, trigger="cron", minute="*/2", kwargs={"manager": manager})

    scheduler.start()


def start_bot():
    # TODO организовать проверку файла с сессией, если нет то сделать подключение и ответить на смс
    logging.basicConfig(level=logging.INFO)
    client = TelegramClient('anon', API_ID, API_HASH)
    client.loop.create_task(__on_start_up())
    logging.info("START BOT")
    client.loop.run_forever()