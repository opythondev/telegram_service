import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.utils.apiexceptions import InsertException
from core.routers import basic

import uvicorn


app = FastAPI()

app.include_router(basic.router)


@app.exception_handler(InsertException)
async def insert_exception_handler(request: Request, exc: InsertException):
    return JSONResponse(
        status_code=420,
        content={
            "message": (
                f"Oops! Seems like {exc.name} raised.\n\n Or something else wrong"
            )
        },
    )


@app.on_event("startup")
async def startup():
    # await database.connect()
    logging.info("start")


@app.on_event("shutdown")
async def shutdown():
    # await database.disconnect()
    logging.info("shutdown")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8083)
