import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

def get_db_url():
    # If running in Docker with local Postgres
    if os.getenv("DOCKER_ENV") == "local":
        return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@db/{settings.DB_NAME}"
    
    # If connecting to Cloud SQL
    if os.getenv("CLOUD_SQL_CONNECTION_NAME"):
        return (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@/"
            f"{settings.DB_NAME}?host=/cloudsql/{settings.CLOUD_SQL_CONNECTION_NAME}"
        )
    
    # Default local development
    return f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@localhost/{settings.DB_NAME}"

engine = create_async_engine(get_db_url(), pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
