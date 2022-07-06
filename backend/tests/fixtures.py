"""Deeper 2022, All Rights Reserved
"""
from typing import Tuple
import pytest
from sanic import Sanic
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from api import create_app
from config import get_current_config
from api.users.models import User
from core.ext import Base


GenericTestSetup = Tuple[Sanic, AsyncSession]


@pytest.fixture(autouse=True)
async def generic_test_setup() -> GenericTestSetup:
    """Set up environment for tests:
        - Clean database
        - Create a test user
        - Return a async database session
        - return
    """
    engine = create_async_engine(get_current_config().DATABASE_URI, echo=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        async with session.begin():
            session.add_all([User(username='test_user', password='12345678')])
            await session.commit()

    return create_app(), async_session
