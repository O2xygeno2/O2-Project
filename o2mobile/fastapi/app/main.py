from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.database.connection import engine, Base
from app.api.v1.routers import api_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME)

@app.on_event("startup")
async def startup():
    """Initialize database connection and create tables"""
    logger.info("Starting up application...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Database initialization failed"
        ) from e

@app.get("/db")
async def check_database_connection():
    """Endpoint to verify database connectivity"""
    try:
        async with engine.connect() as conn:
            result = await conn.execute("SELECT 1")
            if result.scalar() == 1:
                return {
                    "status": "success",
                    "message": "Database connection successful",
                    "db_name": settings.DB_NAME
                }
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "message": "Database connection failed",
                "error": str(e)
            }
        )

@app.get("/")
def read_root():
    """Root endpoint with health check"""
    return {
        "message": "Hello World",
        "service": settings.PROJECT_NAME,
        "status": "running"
    }

# Include API routers
app.include_router(api_router, prefix="/api/v1")

# Add exception handler for database errors
@app.exception_handler(Exception)
async def database_exception_handler(request, exc):
    logger.error(f"Database error occurred: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal database error"}
    )
