from fastapi import Request, APIRouter
from core.models.models import TaskInput

router = APIRouter()


@router.post("/fetch_channels")
async def fetch_channels(request_data: TaskInput):
    return request_data
