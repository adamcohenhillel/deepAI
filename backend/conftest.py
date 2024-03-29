"""Deeper 2022, All Rights Reserved

Fixtures for pytests
"""
from typing import Any, AsyncGenerator, Tuple

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api.app import get_app
from db.models.user import User
from db.neo4j.connector import Neo4jDBConnector
from db.dependencies import get_db_session, get_neo4j_connector
from db.models.base import Base
from settings import settings


@pytest.fixture(scope="session")
def anyio_backend() -> str:
    """Backend for anyio pytest plugin.

    :return: backend name.
    """
    return "asyncio"


@pytest.fixture()
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create engine and databases.

    :yield: new engine.
    """
    engine = create_async_engine(settings.db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    try:
        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest.fixture
async def dbsession(
    _engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession, None]:
    """Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = sessionmaker(
        connection,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session = session_maker()

    # A test user:
    session.add(User(username='test_user', password='Aa12345678!'))
    await session.commit()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture
def fastapi_app(
    dbsession: AsyncSession,
) -> FastAPI:
    """Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    app = get_app()
    app.dependency_overrides[get_db_session] = lambda: dbsession
    app.dependency_overrides[get_neo4j_connector] = lambda: Neo4jDBConnector(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)
    return app


@pytest.fixture
async def client(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> AsyncGenerator[AsyncClient, None]:
    """Fixture that creates client for requesting server.

    :param fastapi_app: the app.

    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture
async def client_and_token(
    fastapi_app: FastAPI,
    anyio_backend: Any,
) -> Tuple[AsyncGenerator[AsyncClient, None], str]:
    """Fixture that creates client for requesting server.

    :param fastapi_app: the app.

    :yield: client for the app.
    """
    async with AsyncClient(app=fastapi_app, base_url='http://test') as async_client:
        response = await async_client.post(
            '/api/users/auth',
            data={'password': 'Aa12345678!', 'username': 'test_user'}
        )
        yield async_client, response.json()['access_token']
