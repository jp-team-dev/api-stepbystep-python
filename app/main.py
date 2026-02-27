from contextlib import asynccontextmanager

from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import content


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="StepByStep API", lifespan=lifespan)

app.include_router(content.router, prefix="/learning", tags=["learning"])


@app.get("/health")
def health():
    return {"status": "ok"}
