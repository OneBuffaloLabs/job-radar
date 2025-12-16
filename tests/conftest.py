import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlmodel import SQLModel

from app.main import app
from app.core.db import get_session, settings

@pytest_asyncio.fixture(scope="function")
async def db_engine():
    # NullPool is still critical here
    engine = create_async_engine(
        settings.DATABASE_URL,
        future=True,
        poolclass=NullPool
    )

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine

    # Explicitly dispose to close connections before the loop closes
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    session_factory = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        yield session

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    app.dependency_overrides[get_session] = lambda: db_session
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()