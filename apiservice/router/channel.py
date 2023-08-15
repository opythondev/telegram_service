from fastapi import APIRouter, Depends
from dependencies import get_token_header
from service.s_channel import ChannelService

router = APIRouter(
    prefix="/channel",
    tags=['channel'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_all_channels/")
async def get_channels_id():
    channel_f = ChannelService()
    data = await channel_f.get_all_channels()

    return {"status": 200,
            "data": data}


@router.get("/get_all_users/")
async def get_all_users(channel_id: int):
    channel_f = ChannelService(channel_id=channel_id)
    data = await channel_f.get_all_users()

    return {"status": 200,
            "length": len(data),
            "data": data}


@router.get("/get_last_msg/")
async def get_last_msg(channel_id: int):
    channel_f = ChannelService(channel_id=channel_id)
    data = await channel_f.get_last_msg()

    return {"status": 200,
            "length": len(data),
            "data": data}
