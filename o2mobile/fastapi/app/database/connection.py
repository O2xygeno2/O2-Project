import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

def get_db_url():
    if os.getenv("CLOUD_SQL_CONNECTION_NAME"):
        # Cloud SQL Production Connection
        return (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@/"
            f"{settings.DB_NAME}?host=/cloudsql/{settings.CLOUD_SQL_CONNECTION_NAME}"
        )
    else:
        # Fallback for local development
        return (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
            f"{os.getenv('DB_HOST', 'localhost')}/{settings.DB_NAME}"
        )

engine = create_async_engine(
    get_db_url(),
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=10,
    echo=False  # Set to True for debugging queries
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
