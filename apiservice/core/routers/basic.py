from fastapi import APIRouter
from core.models.models import TaskInput, TaskOut
from core.celeryservice.main import add_channel_list_to_worker, dummy_task, celery_app
from celery.result import AsyncResult


router = APIRouter()


def _to_task_out(r: AsyncResult) -> TaskOut:
    return TaskOut(id=r.task_id, status=r.status)


@router.get("/start")
def start() -> TaskOut:
    r = dummy_task.delay()
    return _to_task_out(r)


@router.get("/status")
def status(task_id: str) -> TaskOut:
    r = celery_app.AsyncResult(task_id)
    return _to_task_out(r)


@router.get("/tasks")
async def get_tasks():
    tasks = celery_app.control.inspect()
    reserved = tasks.reserved()
    return reserved


@router.post("/fetch_channels")
async def fetch_channels(request_data: TaskInput):
    task = add_channel_list_to_worker.delay(request_data.channels)
    return {"status": 200,
            'task_id': task.task_id,
            "task_status": task.status}
