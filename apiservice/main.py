from fastapi import FastAPI
from router.channel import router as channel_router
from router.task import router as  task_router

app = FastAPI()

app.include_router(channel_router)
app.include_router(task_router)
