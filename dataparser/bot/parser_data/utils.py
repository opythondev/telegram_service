from bot.database.models.task import TaskData
from bot.database.models.task_item import TaskItemData


async def convert_dict_to_task(data: dict) -> TaskData:
    return TaskData(type=data['type'],
                    user_id=data['user_id'],
                    urls=data['urls'],
                    id=data['id'],
                    status=data['status'],
                    create_at=data['create_at'])


async def convert_task_to_dict(task: TaskData) -> dict:
    return {"type": task.type,
            "user_id": task.user_id,
            "urls": task.urls,
            "id": task.id,
            "status": task.status,
            "create_at": str(task.create_at)}


async def convert_dict_to_task_item(task_item: dict) -> TaskItemData:
    return TaskItemData(task_id=task_item['task_id'],
                        target_url=task_item['target_url'],
                        channel_id=task_item['channel_id'],
                        id=task_item['id'],
                        status="created")


async def convert_task_item_to_dict(task_item: TaskItemData) -> dict:
    return {"task_id": task_item.task_id,
            "target_url": task_item.target_url,
            "channel_id": task_item.channel_id,
            "id": task_item.id,
            "status": task_item.status}
