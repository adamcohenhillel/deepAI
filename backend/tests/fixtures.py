"""Deeper 2022, All Rights Reserved
"""
import logging
from typing import Tuple
import pytest
from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api import create_app
from config import get_current_config
from api.users.models import User
from core.ext import Base


GenericTestSetup = Tuple[Sanic, AsyncSession, str]


@pytest.fixture(autouse=True)
async def generic_test_setup() -> GenericTestSetup:
    """Set up environment for tests:
        - Clean database
        - Create a test user
        - Return a async database session
        - return
    """
    logging.info('Setting up test with geenric setup')
    print('********************')
    print(get_current_config().DATABASE_URI)
    print('********************')
    engine = create_async_engine(get_current_config().DATABASE_URI, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([User(username='test_user', password='Aa12345678!')])
            await session.commit()

    api_app = create_app()
    _, response = await api_app.asgi_client.post('/v1/auth', json={'password': 'Aa12345678!', 'username': 'test_user'})
    access_token = response.json.get('access_token', '')
    logging.info('Setup nded')
    yield api_app, async_session, access_token
    # tearDown:
    async_session.close()
