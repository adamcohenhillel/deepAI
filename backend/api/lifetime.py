from asyncio import current_task
from typing import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
import aioredis

from settings import settings
from db.models.base import Base
from db.neo4j.connector import Neo4jDBConnector


def _setup_dbs(app: FastAPI) -> None:
    """Creates connection to the databases

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the app's state property.

    :param app: fastAPI app.
    """
    engine = create_async_engine(settings.db_url, echo=settings.db_echo)
    session_factory = async_scoped_session(
        sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession,
        ),
        scopefunc=current_task,
    )
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
    app.state.neo4j = Neo4jDBConnector(settings.neo4j_uri, settings.neo4j_user, settings.neo4j_password)


def register_startup_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """Actions to run on app startup.

    This function uses fastAPI app to store data
    inthe state, such as db_engine.

    :param app: the fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event('startup')
    async def _startup() -> None:  # noqa: WPS430
        _setup_dbs(app)
        app.state.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        async with app.state.db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        pass  # noqa: WPS420

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """Actions to run on app's shutdown.

    :param app: fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:  # noqa: WPS430
        await app.state.db_engine.dispose()
        await app.state.redis.close()
        pass  # noqa: WPS420

    return _shutdown
