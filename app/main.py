from fastapi import FastAPI

from .database import create_db_and_tables
from .routers import content

app = FastAPI(title="StepByStep API")

app.include_router(content.router, prefix="/learning", tags=["learning"])

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health():
    return {"status": "ok"}
