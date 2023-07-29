from fastapi import APIRouter, Depends
from dependencies import get_token_header
from database.models.task import TaskData
from service.s_task import STask
from .utils import convert_task_to_dict

router = APIRouter(
    prefix="/task",
    tags=['task'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.post("/add_task/")
async def create_new_task(task_data: TaskData):
    task = STask(task_data=await convert_task_to_dict(task_data))
    data = await task.send_task_to_bot()

    return {"status": 200,
            "data": data}

