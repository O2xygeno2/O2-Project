import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

def get_db_url():
    if os.getenv("CLOUD_SQL_CONNECTION_NAME"):
        # Cloud Run environment
        return (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@/"
            f"{settings.DB_NAME}?host=/cloudsql/{settings.CLOUD_SQL_CONNECTION_NAME}"
        )
    else:
        # Local development environment
        return (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
            f"localhost/{settings.DB_NAME}"
        )

engine = create_async_engine(get_db_url(), pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
