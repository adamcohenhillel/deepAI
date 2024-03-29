from asyncio import current_task
from typing import Awaitable, Callable

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker
# import aioredis

from settings import settings
from db.models.base import Base
from db.models.rooms import Room, RoomMessage
from db.models.user import User
from db.neo4j.connector import Neo4jDBConnector


def _setup_dbs(app: FastAPI) -> None:
    """Creates connection to the databases

    This function creates SQLAlchemy engine instance,
    session_factory for creating sessions
    and stores them in the app's state property.

    :param app: fastAPI app.
    """
    engine = create_async_engine(settings.db_url, echo=settings.db_echo, isolation_level="AUTOCOMMIT")
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
    async def _startup() -> None:
        _setup_dbs(app)
        # app.state.redis = aioredis.from_url(settings.redis_url, decode_responses=True)
        async with app.state.db_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        session = app.state.db_session_factory()
        room = Room()
        session.add(User(username='adam', password='thisisAstringPass1!'))
        await session.commit()
        room.messages.append(RoomMessage(text='hello', user_id=1))
        room.messages.append(RoomMessage(text='heyy whats up', user_id=1))
        room.messages.append(RoomMessage(text='yee im all good', user_id=1))
        room.messages.append(RoomMessage(text='cool me too', user_id=1))
        room.messages.append(RoomMessage(text='how are ya feeling?', user_id=1))
        session.add(room)
        session.add(Room())
        session.add(Room())
        await session.commit()

    return _startup


def register_shutdown_event(app: FastAPI) -> Callable[[], Awaitable[None]]:
    """Actions to run on app's shutdown.

    :param app: fastAPI app.
    :return: function that actually performs actions.
    """

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await app.state.db_engine.dispose()
        # await app.state.redis.close()

    return _shutdown
