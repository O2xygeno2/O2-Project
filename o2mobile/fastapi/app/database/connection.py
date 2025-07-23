import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def get_db_url():
    if os.getenv("CLOUD_SQL_CONNECTION_NAME"):
        # Cloud Run environment
        connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
        db_user = os.getenv("POSTGRES_USER", settings.DB_USER)
        db_pass = os.getenv("POSTGRES_PASSWORD", settings.DB_PASS)
        db_name = os.getenv("POSTGRES_DB_NAME", settings.DB_NAME)
        
        socket_path = f"/cloudsql/{connection_name}"
        
        # Verify socket path exists (for debugging)
        if not os.path.exists(socket_path):
            logger.warning(f"Cloud SQL socket path not found: {socket_path}")
        
        return (
            f"postgresql+asyncpg://{db_user}:{db_pass}@/"
            f"{db_name}?host={socket_path}"
        )
    else:
        # Local development environment
        return (
            f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@"
            f"localhost/{settings.DB_NAME}"
        )

try:
    engine = create_async_engine(
        get_db_url(),
        pool_pre_ping=True,
        echo=True  # Enable SQL logging for debugging
    )
    AsyncSessionLocal = sessionmaker(
        engine, 
        class_=AsyncSession, 
        expire_on_commit=False
    )
    Base = declarative_base()
except Exception as e:
    logger.error(f"Failed to initialize database engine: {str(e)}")
    raise

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
