import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

"""Database engine + session utilities.

Schema management is handled by Alembic migrations (see alembic/).
"""

_engine: AsyncEngine | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is not None:
        return _engine

    db_url = os.getenv("MYSQL_DB_ASYNC_URL")
    if not db_url:
        raise RuntimeError("MYSQL_DB_ASYNC_URL environment variable is not set")

    _engine = create_async_engine(db_url, echo=True)
    return _engine

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    engine = get_engine()
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as session:
        yield session
