"""Deeper 2022, All Rights Reserved
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from redis.asyncio import Redis

from db.neo4j.connector import Neo4jDBConnector


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Create and get postgresql database session.

    :param request: current request

    :yield: database session
    """
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        yield session
    finally:
        await session.commit()
        await session.close()


async def get_neo4j_connector(request: Request) -> Neo4jDBConnector:
    """Create and get neo4j session

    :param request: current request

    :yield: neo4j connector
    """
    return request.app.state.neo4j


async def get_redis_connection(request: Request) -> AsyncGenerator[Redis, None]:
    """Get redis client.

    This dependency aquires connection from pool.

    :param request: current request.

    :yield: redis client.
    """
    return request.app.state.redis