from random import choice
from .task_manager import manager


async def job_item():
    print("JOB IN WORKER")


async def create_fake_task():
    print("TICK")
    FAKE_DATA = {
        "url": ["https://t.me/YoutubePronin", "https://t.me/fastapiru", "https://t.me/trueDjangoChannel",
                "https://t.me/openvocallessons", "https://t.me/progbook", "https://t.me/progbook2",
                "https://t.me/backenderrr", "https://t.me/sasha_vocal"],
        "target": ['test'],
        "user_id": 233652006
    }

    for job_k, job_v in FAKE_DATA.items():
        t = await manager.create_task_(job_item, trigger="now")
        await manager.add_local_task(t)
