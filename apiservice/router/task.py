from fastapi import APIRouter, Depends
from dependencies import get_token_header
from database.models.task import TaskData
from tasks import add_task_to_queue

router = APIRouter(
    prefix="/task",
    tags=['task'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add_task/")
async def create_new_task(task_data: TaskData):
    await add_task_to_queue(task_data=task_data)
