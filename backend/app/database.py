from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings as global_settings
from app.utils.logging import AppLogger

logger = AppLogger().get_logger()

engine = create_async_engine(
    global_settings.asyncpg_url.unicode_string(),
    future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)

engine_sync = create_engine(
    global_settings.psycopg2_url.unicode_string(),
    # future=True,
    echo=True,
)

# expire_on_commit=False will prevent attributes from being expired
# after commit.
SessionFactory = sessionmaker(
    engine_sync,
    autoflush=False,
    expire_on_commit=False,
)


class DatabaseSessionManager:
    def __init__(self):
        self.session = None

    def __enter__(self):
        self.session = SessionFactory()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()


# Dependency
async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        try:
            yield session
        finally:
            await session.close()
