import logging

from telethon import TelegramClient

from bot.configs.env import API_ID, API_HASH
from bot.task.task_manager import scheduler, manager, check_tasks, add_task_to_local_queue


async def __on_start_up():

    logging.info("INIT on_start_up")

    scheduler.add_job(func=check_tasks, trigger="cron", minute="*/1", kwargs={"manager": manager})
    scheduler.add_job(func=add_task_to_local_queue, trigger="cron", minute="*/1")

    scheduler.start()


def start_bot():
    logging.basicConfig(level=logging.INFO)
    client = TelegramClient('anon', API_ID, API_HASH)
    client.loop.create_task(__on_start_up())
    logging.info("START BOT -> dataparser")
    client.loop.run_forever()


if __name__ == "__main__":
    start_bot()
