from fastapi import APIRouter, Depends
from dependencies import get_token_header


router = APIRouter(
    prefix="/group",
    tags=['group'],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
