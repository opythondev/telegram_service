from fastapi import FastAPI
from router.group import router as group_router

app = FastAPI()

app.include_router(group_router)
