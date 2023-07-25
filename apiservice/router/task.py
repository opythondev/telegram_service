from fastapi import APIRouter, Depends
from dependencies import get_token_header
from service.s_task import STask
from database.models.task import TaskData

router = APIRouter(
    prefix="/task",
    tags=['task'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add_task/")
async def create_new_task(task_data: TaskData, urls: str):
    task = STask(task_data=task_data, urls=urls)
    return await task.add_task_event()
