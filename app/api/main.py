from fastapi import FastAPI
from .routers.code import router


app = FastAPI()

app.include_router(router, prefix="/api/code", tags=["code"])
