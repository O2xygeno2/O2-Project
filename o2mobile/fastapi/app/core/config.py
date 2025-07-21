from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI PostgreSQL"
    
    # For Cloud Run + Cloud SQL
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_SOCKET_DIR: str = os.getenv("DB_SOCKET_DIR", "/cloudsql")
    CLOUD_SQL_CONNECTION_NAME: str = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    
    # For local development
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    
    DEBUG: bool = False

    class Config:
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        if self.CLOUD_SQL_CONNECTION_NAME:
            return (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@/{self.DB_NAME}"
                f"?host={self.DB_SOCKET_DIR}/{self.CLOUD_SQL_CONNECTION_NAME}"
                "&async_fallback=True"  # Important for PostGIS with asyncpg
            )
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.DB_NAME}"
            "?async_fallback=True"
        )

settings = Settings()
