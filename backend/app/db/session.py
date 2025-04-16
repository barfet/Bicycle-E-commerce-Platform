from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator # Import AsyncGenerator
from app.config import settings

# Ensure the DATABASE_URL uses the asyncpg driver for the async engine
DATABASE_URL_ASYNC = settings.DATABASE_URL
if DATABASE_URL_ASYNC and not DATABASE_URL_ASYNC.startswith("postgresql+asyncpg"):
    DATABASE_URL_ASYNC = DATABASE_URL_ASYNC.replace("postgresql://", "postgresql+asyncpg://")

# Create the SQLAlchemy async engine
async_engine = create_async_engine(DATABASE_URL_ASYNC, pool_pre_ping=True, echo=False) # echo=False generally good for prod

# Create a configured "AsyncSession" class
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Dependency to get async DB session (used in API endpoints)
async def get_db() -> AsyncGenerator[AsyncSession, None]: # Make it async
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback() # Rollback on exception within endpoint
            raise
        finally:
            await session.close() # Ensure session is closed 