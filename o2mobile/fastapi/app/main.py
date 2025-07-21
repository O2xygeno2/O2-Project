from fastapi import FastAPI
from app.core.config import settings
from app.database.connection import engine, Base
from app.api.v1.routers import api_router

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup():
    # Create db tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router, prefix="/api/v1")
