from fastapi import APIRouter, Depends
from dependencies import get_token_header


router = APIRouter(
    prefix="/group",
    tags=['group'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

groups = {}


@router.get("/{group_id}")
async def get_group_by_id(group_id: int):
    try:
        return {groups[group_id]}
    except Exception:
        return {}


@router.post("/add_group/{group_id}")
async def add_task_group_by_id(user_id: int, group_id: int):

    groups[group_id] = {"user_id": user_id, "group_id": group_id}

    return {"status": "Group add success"}


@router.get("/get/user_id/{user_id}")
async def get_groups_by_uid(user_id: int):
    result = []
    for k, v in groups.items():
        if v[user_id]:
            result.append(k)

    return result

