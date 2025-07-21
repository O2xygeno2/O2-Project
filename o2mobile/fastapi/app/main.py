from fastapi import FastAPI
from app.core.config import settings
from app.database.connection import engine, Base
from app.api.v1.routers import api_router

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup():
    return {"message": "Start Up"}


@app.get("/db")
def connect_database():
    # Create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"DB Says": "Hello Shivank"}

@app.get("/")
def read_root():
    return {"message": "Hello World"}

app.include_router(api_router, prefix="/api/v1")
