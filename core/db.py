import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

"""Database engine + session utilities.

Schema management is handled by Alembic migrations (see alembic/).
"""

_engine: AsyncEngine | None = None
_SessionLocal: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    global _engine
    if _engine is not None:
        return _engine

    db_url = os.getenv("MYSQL_DB_ASYNC_URL")
    if not db_url:
        raise RuntimeError("MYSQL_DB_ASYNC_URL environment variable is not set")

    _engine = create_async_engine(db_url, echo=True)
    return _engine


def get_sessionmaker() -> async_sessionmaker[AsyncSession]:
    global _SessionLocal
    if _SessionLocal is not None:
        return _SessionLocal

    engine = get_engine()
    _SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return _SessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    SessionLocal = get_sessionmaker()
    async with SessionLocal() as session:
        yield session